"""Giao diện web cho ReAct agent (Streamlit).

Chạy:
    streamlit run app.py

Mỗi câu hỏi được xử lý độc lập (agent chưa nhớ các lượt trước). Trace Thought → Action → Observation
hiện theo thời gian thực trong khung "Agent đang làm việc", rồi thu gọn lại khi có câu trả lời.
"""
from __future__ import annotations

import json

import openai
import streamlit as st

import agent
from tools import CITIES

st.set_page_config(page_title="Trợ lý du lịch ReAct", page_icon="🧭", layout="centered")


def format_event(kind: str, step: int, payload) -> str | None:
    """Đổi một sự kiện của agent thành markdown. Trả None nếu không có gì để hiển thị."""
    if kind == "thought":
        return f"💭 **Thought {step}:** {payload}" if payload.strip() else None
    if kind == "action":
        args = json.dumps(payload["args"], ensure_ascii=False)
        return f"🔧 **Action {step}:** `{payload['tool']}({args})`"
    if kind == "observation":
        icon = "⚠️" if str(payload).startswith("ERROR") else "👁️"
        return f"{icon} **Observation {step}:** `{payload}`"
    return None


def render_trace(container, trace: list[str]) -> None:
    for line in trace:
        container.markdown(line)


# ---------------------------------------------------------------- thanh bên
with st.sidebar:
    st.header("Thông tin agent")
    st.markdown(f"**Model:** `{agent.MODEL}`")
    st.markdown(f"**Giới hạn vòng lặp:** {agent.MAX_ITERATIONS}")
    st.markdown("**Thành phố hỗ trợ:**")
    for city in CITIES:
        st.markdown(f"- {city}")
    st.markdown("**Tool:** " + ", ".join(f"`{t['name']}`" for t in agent.TOOLS))
    if st.button("Xóa hội thoại", use_container_width=True):
        st.session_state.history = []
        st.rerun()

st.title("🧭 Trợ lý du lịch")
st.caption("Hỏi về ngày, thời tiết hoặc nên mặc gì. Agent tự gọi tool và hiển thị từng bước suy luận.")

# ---------------------------------------------------------------- lịch sử
history: list[dict] = st.session_state.setdefault("history", [])
for msg in history:
    with st.chat_message(msg["role"]):
        if msg.get("trace"):
            with st.expander(f"Xem {len(msg['trace'])} bước agent đã làm"):
                render_trace(st, msg["trace"])
        st.markdown(msg["content"])

# ---------------------------------------------------------------- câu hỏi mới
if question := st.chat_input("Ví dụ: Ngày mai ở Đà Nẵng nên mặc gì?"):
    history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        status = st.status("Agent đang làm việc...", expanded=True)
        trace: list[str] = []

        def on_event(kind: str, step: int, payload) -> None:
            line = format_event(kind, step, payload)
            if line:
                trace.append(line)
                status.markdown(line)

        try:
            answer = agent.run_agent(question, on_event=on_event)
            status.update(label=f"Xong sau {len(trace)} bước" if trace else "Trả lời trực tiếp, không cần tool",
                          state="complete", expanded=False)
        except openai.AuthenticationError:
            answer = "⚠️ API key không hợp lệ. Kiểm tra `GROQ_API_KEY` trong file `.env`."
            status.update(label="Lỗi xác thực", state="error")
        except openai.APIError as e:
            answer = f"⚠️ Lỗi khi gọi API: {e}"
            status.update(label="Lỗi khi gọi API", state="error")
        except SystemExit as e:  # call_model dùng sys.exit khi thiếu key
            answer = f"⚠️ {e}"
            status.update(label="Thiếu cấu hình", state="error")
        st.markdown(answer)

    history.append({"role": "assistant", "content": answer, "trace": trace})
