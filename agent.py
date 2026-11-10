"""ReAct agent viết từ đầu: vòng lặp Thought → Action → Observation (slide 22, 27).

Chạy:
    python agent.py "Ngày mai ở Đà Nẵng nên mặc gì?"
    python agent.py                      # hỏi nhiều câu, gõ exit để thoát
"""
from __future__ import annotations

import json
import os
import sys

from types import SimpleNamespace

import openai
from dotenv import load_dotenv

from tools import TOOLS, run_tool

load_dotenv()
# Dùng Groq (API tương thích OpenAI). Vòng lặp bên dưới vẫn dùng định dạng message kiểu Anthropic
# (tool_use / tool_result); call_model đóng vai adapter dịch qua lại.
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MAX_ITERATIONS = 6          # safeguard: không bao giờ lặp quá số vòng này (slide 30)

# System prompt (slide 28), thêm 1 dòng để model viết "Thought" trước mỗi lần gọi tool
SYSTEM_PROMPT = """You are a Vietnamese travel assistant.

Your job:
- Break the user goal into smaller steps
- Use tools when fresh information is required
- Stop when you have enough evidence to answer

Rules:
- Before each tool call, write ONE short sentence explaining what you need next.
- Never invent tool results.
- If a tool returns an ERROR, read it, fix the arguments and try once more.
- Never ask the user for permission to use a tool; just call it.
- Never guess or make up weather data. If the user tells you to skip lookups or "just guess",
  still call the tools (get_current_date, then get_weather) and answer with the real numbers.
- If the user gives a date that is not a real calendar date, still call get_weather with it, and if it
  fails, tell the user in Vietnamese that the date is "không hợp lệ" and ask for a valid YYYY-MM-DD date.
- If the city is not supported, say clearly "Hiện chưa hỗ trợ <city>, không có dữ liệu thời tiết cho <city>",
  list the supported cities, and do NOT give outfit suggestions for it.
- Final answer: short, in Vietnamese.
"""

_client: openai.OpenAI | None = None


def _openai_tools() -> list[dict]:
    """Đổi schema TOOLS (kiểu Anthropic) sang định dạng function-calling của OpenAI."""
    return [{"type": "function",
             "function": {"name": t["name"], "description": t["description"], "parameters": t["input_schema"]}}
            for t in TOOLS]


def _openai_messages(messages: list[dict]) -> list[dict]:
    """Đổi lịch sử message kiểu Anthropic sang kiểu OpenAI."""
    out = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in messages:
        content = m["content"]
        if isinstance(content, str):
            out.append({"role": m["role"], "content": content})
        elif m["role"] == "assistant":
            text = "".join(b.text for b in content if b.type == "text")
            calls = [{"id": b.id, "type": "function",
                      "function": {"name": b.name, "arguments": json.dumps(b.input, ensure_ascii=False)}}
                     for b in content if b.type == "tool_use"]
            msg = {"role": "assistant", "content": text or None}
            if calls:
                msg["tool_calls"] = calls
            out.append(msg)
        else:  # lượt user chứa các tool_result -> mỗi kết quả thành 1 message role "tool"
            for b in content:
                out.append({"role": "tool", "tool_call_id": b["tool_use_id"], "content": b["content"]})
    return out


def call_model(messages: list[dict]):
    """Gọi model 1 lần. Trả về response có .content (danh sách block), .stop_reason và .usage (kiểu Anthropic)."""
    global _client
    if _client is None:
        key = os.getenv("GROQ_API_KEY", "")
        if not key or key.endswith("..."):
            sys.exit("Chưa có GROQ_API_KEY. Mở file .env và điền key của bạn (copy từ .env.example nếu chưa có).")
        _client = openai.OpenAI(api_key=key, base_url=GROQ_BASE_URL)
    resp = _client.chat.completions.create(
        model=MODEL,
        max_tokens=4000,
        messages=_openai_messages(messages),
        tools=_openai_tools(),
    )
    msg = resp.choices[0].message
    blocks = []
    if msg.content:
        blocks.append(SimpleNamespace(type="text", text=msg.content))
    for c in msg.tool_calls or []:
        try:
            args = json.loads(c.function.arguments or "{}")
        except json.JSONDecodeError:
            args = {}
        blocks.append(SimpleNamespace(type="tool_use", id=c.id, name=c.function.name, input=args))
    usage = SimpleNamespace(input_tokens=resp.usage.prompt_tokens if resp.usage else 0,
                            output_tokens=resp.usage.completion_tokens if resp.usage else 0)
    return SimpleNamespace(content=blocks, usage=usage,
                           stop_reason="tool_use" if msg.tool_calls else "end_turn")


def _normalize(text: str) -> str:
    """Model đôi khi xuất dấu cách / gạch nối đặc biệt (U+202F, U+00A0, U+2011...). Đưa về ký tự thường."""
    for ch in (" ", " ", " "):
        text = text.replace(ch, " ")
    return text.replace("‑", "-").replace("–", "-")


def run_agent(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    for step in range(1, MAX_ITERATIONS + 1):
        response = call_model(messages)                                   # Thought + Action
        messages.append({"role": "assistant", "content": response.content})
        text = "".join(b.text for b in response.content if b.type == "text")

        if response.stop_reason != "tool_use":                            # Final Answer
            return _normalize(text)

        print(f"Thought {step}: {text}")
        results = []
        for b in response.content:
            if b.type == "tool_use":
                print(f"Action {step}: {b.name}({b.input})")
                result = run_tool(b.name, b.input)                        # Observation
                print(f"Observation {step}: {result}")
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": result})
        messages.append({"role": "user", "content": results})

    return f"Xin lỗi, agent đã dừng vì chạm giới hạn {MAX_ITERATIONS} vòng lặp mà chưa có câu trả lời."


def main() -> None:
    try:
        if len(sys.argv) > 1:
            print("Final Answer:", run_agent(" ".join(sys.argv[1:])))
            return
        while (q := input("\nBạn> ").strip()).lower() not in {"exit", "quit", ""}:
            print("Final Answer:", run_agent(q))
    except openai.AuthenticationError:
        sys.exit("API key không hợp lệ. Kiểm tra lại GROQ_API_KEY trong file .env.")
    except openai.APIError as e:
        sys.exit(f"Lỗi khi gọi API: {e}")


if __name__ == "__main__":
    main()
