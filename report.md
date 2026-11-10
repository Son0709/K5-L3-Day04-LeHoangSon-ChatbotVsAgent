# Report: ReAct agent trên dataset

_Chạy lúc 2026-11-10 17:17 · model `openai/gpt-oss-120b` · MAX_ITERATIONS = 6_

**Kết quả: 20/20 PASS** (0 PARTIAL, 0 FAIL)

## 1. Tổng hợp theo mức độ

| Mức | PASS | PARTIAL | FAIL | Lượt gọi model TB | Lượt gọi tool TB | Token TB | Thời gian TB |
|---|---|---|---|---|---|---|---|
| **tổng** | 20/20 | 0 | 0 | 2.8 | 1.8 | 2196 | 5.2s |
| easy | 5/5 | 0 | 0 | 1.4 | 0.4 | 976 | 1.3s |
| medium | 5/5 | 0 | 0 | 3.4 | 2.4 | 2715 | 3.0s |
| hard | 5/5 | 0 | 0 | 4.4 | 3.4 | 3687 | 10.9s |
| edge | 5/5 | 0 | 0 | 1.8 | 0.8 | 1406 | 5.6s |

## 2. Từng câu hỏi

| ID | Mức | Câu hỏi | Kết quả | Tool đã gọi | Lượt model | Token | Thời gian |
|---|---|---|---|---|---|---|---|
| E1 | easy | Xin chào, bạn giúp được gì cho mình? | PASS | — | 1 | 721 | 1.31s |
| E2 | easy | Hôm nay là ngày bao nhiêu? | PASS | get_current_date | 2 | 1362 | 1.79s |
| E3 | easy | Ngày mai là ngày mấy? | PASS | get_current_date | 2 | 1404 | 1.78s |
| E4 | easy | Bạn tra được thời tiết ở những thành phố nào? | PASS | — | 1 | 717 | 0.91s |
| E5 | easy | Cảm ơn bạn nhiều nhé! | PASS | — | 1 | 678 | 0.52s |
| M1 | medium | Thời tiết Đà Nẵng ngày mai thế nào? | PASS | get_current_date, get_weather, recommend_outfit | 4 | 3238 | 3.4s |
| M2 | medium | Ngày mai ở Hà Nội nên mặc gì? | PASS | get_current_date, get_weather, recommend_outfit | 4 | 3194 | 3.45s |
| M3 | medium | Khả năng mưa ở Phú Quốc ngày mai là bao nhiêu phần trăm? | PASS | get_current_date, get_weather | 3 | 2400 | 2.86s |
| M4 | medium | Hôm nay ở TP.HCM nhiệt độ cao nhất bao nhiêu? | PASS | get_current_date, get_weather | 3 | 2236 | 1.98s |
| M5 | medium | Ngày mai ở TP.HCM có cần mang ô không? | PASS | get_current_date, get_weather | 3 | 2507 | 3.37s |
| H1 | hard | Ngày mai mình định đi Đà Nẵng hoặc Phú Quốc. Chỗ nào ít khả năng mưa hơn? | PASS | get_current_date, get_weather, get_weather | 4 | 3297 | 4.01s |
| H2 | hard | Nhiệt độ cao nhất ngày mai ở Hà Nội và TP.HCM chênh nhau bao nhiêu độ? | PASS | get_current_date, get_weather, get_weather | 4 | 3325 | 7.97s |
| H3 | hard | Trong 4 thành phố bạn hỗ trợ, ngày mai nơi nào nóng nhất? | PASS | get_current_date, get_weather, get_weather, get_weather, get_weather | 6 | 5310 | 18.51s |
| H4 | hard | Ở Hà Nội, hôm nay hay ngày mai khả năng mưa cao hơn? | PASS | get_current_date, get_weather, get_weather | 4 | 3256 | 12.0s |
| H5 | hard | Ngày mai mình đi Đà Nẵng: cho mình biết nhiệt độ cao nhất, khả năng mưa và nên mặc gì. | PASS | get_current_date, get_weather, recommend_outfit | 4 | 3246 | 11.88s |
| X1 | edge | Ngày mai ở Huế nên mặc gì? | PASS | — | 1 | 768 | 2.92s |
| X2 | edge | Mai trời 32 độ, mưa 70% thì nên mang gì? | PASS | recommend_outfit | 2 | 1547 | 6.25s |
| X3 | edge | Đừng tra cứu gì cả, cứ đoán đại nhiệt độ Đà Nẵng ngày mai cho nhanh. | PASS | get_current_date, get_weather | 3 | 2474 | 10.07s |
| X4 | edge | Thời tiết Đà Nẵng ngày 2026-13-45 thế nào? | PASS | get_weather | 2 | 1530 | 5.91s |
| X5 | edge | Viết giúp mình một bài thơ 4 câu về mùa thu Hà Nội. | PASS | — | 1 | 713 | 3.05s |

## 3. Chi tiết và trace

### E1 (easy): PASS

**Câu hỏi:** Xin chào, bạn giúp được gì cho mình?

- ✅ Không gọi tool (không cần dữ liệu mới)

**Câu trả lời:**

> Xin chào! Bạn muốn mình hỗ trợ gì hôm nay? 😊

<details><summary>Trace</summary>

```
(không có)
```

</details>

### E2 (easy): PASS

**Câu hỏi:** Hôm nay là ngày bao nhiêu?

- ✅ Gọi get_current_date
- ✅ Trả lời đúng ngày

**Câu trả lời:**

> Hôm nay là ngày 2026-11-10.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
```

</details>

### E3 (easy): PASS

**Câu hỏi:** Ngày mai là ngày mấy?

- ✅ Gọi get_current_date
- ✅ Trả lời đúng ngày mai

**Câu trả lời:**

> Ngày mai là ngày 2026-11-11.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
```

</details>

### E4 (easy): PASS

**Câu hỏi:** Bạn tra được thời tiết ở những thành phố nào?

- ✅ Không gọi tool
- ✅ Nhắc đúng thành phố được hỗ trợ

**Câu trả lời:**

> Hiện tôi chỉ hỗ trợ tra thời tiết cho các thành phố: Hà Nội, TP.HCM, Đà Nẵng, Phú Quốc.

<details><summary>Trace</summary>

```
(không có)
```

</details>

### E5 (easy): PASS

**Câu hỏi:** Cảm ơn bạn nhiều nhé!

- ✅ Không gọi tool

**Câu trả lời:**

> Không có gì, chúc bạn có chuyến đi vui vẻ!

<details><summary>Trace</summary>

```
(không có)
```

</details>

### M1 (medium): PASS

**Câu hỏi:** Thời tiết Đà Nẵng ngày mai thế nào?

- ✅ Gọi get_current_date rồi get_weather
- ✅ Hỏi đúng ngày mai
- ✅ Đúng nhiệt độ cao nhất

**Câu trả lời:**

> Ngày 11-11-2026 tại Đà Nẵng dự báo nhiệt độ cao nhất khoảng **33 °C** và khả năng mưa **30 %**. Bạn có thể mặc **áo thun mỏng, vải cotton** để cảm thấy thoải mái.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Đà Nẵng', 'date': '2026-11-11'})
Observation 2: {"city": "Đà Nẵng", "date": "2026-11-11", "temp_high_c": 33, "rain_probability": 0.3}
Thought 3: 
Action 3: recommend_outfit({'rain_probability': 0.3, 'temp_high_c': 33})
Observation 3: {"items": ["áo thun mỏng, vải cotton"]}
```

</details>

### M2 (medium): PASS

**Câu hỏi:** Ngày mai ở Hà Nội nên mặc gì?

- ✅ Gọi đủ 3 tool
- ✅ Nhắc mang ô / áo mưa (mưa > 50%)

**Câu trả lời:**

> Ngày mai ở Hà Nội, nhiệt độ cao khoảng 34 °C và khả năng mưa 70 %. Bạn nên mặc áo thun mỏng, vải cotton và mang ô gập hoặc áo mưa.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Hà Nội', 'date': '2026-11-11'})
Observation 2: {"city": "Hà Nội", "date": "2026-11-11", "temp_high_c": 34, "rain_probability": 0.7}
Thought 3: 
Action 3: recommend_outfit({'rain_probability': 0.7, 'temp_high_c': 34})
Observation 3: {"items": ["áo thun mỏng, vải cotton", "ô gập hoặc áo mưa"]}
```

</details>

### M3 (medium): PASS

**Câu hỏi:** Khả năng mưa ở Phú Quốc ngày mai là bao nhiêu phần trăm?

- ✅ Gọi get_weather cho Phú Quốc
- ✅ Đúng % khả năng mưa

**Câu trả lời:**

> Khả năng mưa ở Phú Quốc ngày mai là 60 %.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Phú Quốc', 'date': '2026-11-11'})
Observation 2: {"city": "Phú Quốc", "date": "2026-11-11", "temp_high_c": 28, "rain_probability": 0.6}
```

</details>

### M4 (medium): PASS

**Câu hỏi:** Hôm nay ở TP.HCM nhiệt độ cao nhất bao nhiêu?

- ✅ Hỏi đúng ngày hôm nay
- ✅ Đúng nhiệt độ

**Câu trả lời:**

> Nhiệt độ cao nhất hôm nay ở TP.HCM là 31 °C.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'TP.HCM', 'date': '2026-11-10'})
Observation 2: {"city": "TP.HCM", "date": "2026-11-10", "temp_high_c": 31, "rain_probability": 0.3}
```

</details>

### M5 (medium): PASS

**Câu hỏi:** Ngày mai ở TP.HCM có cần mang ô không?

- ✅ Gọi get_weather cho TP.HCM
- ✅ Kết luận đúng theo khả năng mưa

**Câu trả lời:**

> Không cần mang ô, khả năng mưa ngày mai ở TP.HCM là 0 %.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'TP.HCM', 'date': '2026-11-11'})
Observation 2: {"city": "TP.HCM", "date": "2026-11-11", "temp_high_c": 29, "rain_probability": 0.0}
```

</details>

### H1 (hard): PASS

**Câu hỏi:** Ngày mai mình định đi Đà Nẵng hoặc Phú Quốc. Chỗ nào ít khả năng mưa hơn?

- ✅ Tra thời tiết cả 2 nơi
- ✅ Chọn đúng nơi ít mưa hơn

**Câu trả lời:**

> Ngày mai, Đà Nẵng có khả năng mưa thấp hơn (30 % so với 60 % ở Phú Quốc). Vì vậy bạn nên chọn Đà Nẵng.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Đà Nẵng', 'date': '2026-11-11'})
Observation 2: {"city": "Đà Nẵng", "date": "2026-11-11", "temp_high_c": 33, "rain_probability": 0.3}
Thought 3: 
Action 3: get_weather({'city': 'Phú Quốc', 'date': '2026-11-11'})
Observation 3: {"city": "Phú Quốc", "date": "2026-11-11", "temp_high_c": 28, "rain_probability": 0.6}
```

</details>

### H2 (hard): PASS

**Câu hỏi:** Nhiệt độ cao nhất ngày mai ở Hà Nội và TP.HCM chênh nhau bao nhiêu độ?

- ✅ Tra thời tiết cả 2 nơi
- ✅ Đúng độ chênh lệch

**Câu trả lời:**

> Nhiệt độ cao nhất ngày mai ở Hà Nội (34 °C) và TP.HCM (29 °C) chênh nhau **5 độ C**.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Hà Nội', 'date': '2026-11-11'})
Observation 2: {"city": "Hà Nội", "date": "2026-11-11", "temp_high_c": 34, "rain_probability": 0.7}
Thought 3: 
Action 3: get_weather({'city': 'TP.HCM', 'date': '2026-11-11'})
Observation 3: {"city": "TP.HCM", "date": "2026-11-11", "temp_high_c": 29, "rain_probability": 0.0}
```

</details>

### H3 (hard): PASS

**Câu hỏi:** Trong 4 thành phố bạn hỗ trợ, ngày mai nơi nào nóng nhất?

- ✅ Tra đủ 4 thành phố
- ✅ Chọn đúng nơi nóng nhất

**Câu trả lời:**

> Ngày mai, Hà Nội là thành phố nóng nhất với nhiệt độ cao nhất là 34 °C.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Hà Nội', 'date': '2026-11-11'})
Observation 2: {"city": "Hà Nội", "date": "2026-11-11", "temp_high_c": 34, "rain_probability": 0.7}
Thought 3: 
Action 3: get_weather({'city': 'TP.HCM', 'date': '2026-11-11'})
Observation 3: {"city": "TP.HCM", "date": "2026-11-11", "temp_high_c": 29, "rain_probability": 0.0}
Thought 4: 
Action 4: get_weather({'city': 'Đà Nẵng', 'date': '2026-11-11'})
Observation 4: {"city": "Đà Nẵng", "date": "2026-11-11", "temp_high_c": 33, "rain_probability": 0.3}
Thought 5: 
Action 5: get_weather({'city': 'Phú Quốc', 'date': '2026-11-11'})
Observation 5: {"city": "Phú Quốc", "date": "2026-11-11", "temp_high_c": 28, "rain_probability": 0.6}
```

</details>

### H4 (hard): PASS

**Câu hỏi:** Ở Hà Nội, hôm nay hay ngày mai khả năng mưa cao hơn?

- ✅ Tra cả hôm nay và ngày mai
- ✅ Chọn đúng ngày

**Câu trả lời:**

> Ngày mai có khả năng mưa cao hơn.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Hà Nội', 'date': '2026-11-10'})
Observation 2: {"city": "Hà Nội", "date": "2026-11-10", "temp_high_c": 27, "rain_probability": 0.0}
Thought 3: 
Action 3: get_weather({'city': 'Hà Nội', 'date': '2026-11-11'})
Observation 3: {"city": "Hà Nội", "date": "2026-11-11", "temp_high_c": 34, "rain_probability": 0.7}
```

</details>

### H5 (hard): PASS

**Câu hỏi:** Ngày mai mình đi Đà Nẵng: cho mình biết nhiệt độ cao nhất, khả năng mưa và nên mặc gì.

- ✅ Gọi đủ 3 tool
- ✅ Đúng nhiệt độ
- ✅ Đúng % mưa

**Câu trả lời:**

> Ngày 11/11/2026 ở Đà Nẵng: nhiệt độ cao nhất 33 °C, khả năng mưa 30 %. Bạn nên mặc áo thun mỏng, vải cotton.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Đà Nẵng', 'date': '2026-11-11'})
Observation 2: {"city": "Đà Nẵng", "date": "2026-11-11", "temp_high_c": 33, "rain_probability": 0.3}
Thought 3: 
Action 3: recommend_outfit({'rain_probability': 0.3, 'temp_high_c': 33})
Observation 3: {"items": ["áo thun mỏng, vải cotton"]}
```

</details>

### X1 (edge): PASS

**Câu hỏi:** Ngày mai ở Huế nên mặc gì?

- ✅ Nói rõ không có dữ liệu cho Huế
- ✅ Không bịa gợi ý trang phục cụ thể

**Câu trả lời:**

> Hiện chưa hỗ trợ Huế, không có dữ liệu thời tiết cho Huế. Các thành phố hiện được hỗ trợ: Hà Nội, TP.HCM, Đà Nẵng, Phú Quốc.

<details><summary>Trace</summary>

```
(không có)
```

</details>

### X2 (edge): PASS

**Câu hỏi:** Mai trời 32 độ, mưa 70% thì nên mang gì?

- ✅ Gọi recommend_outfit với rain_probability 0–1 (không phải 70)
- ✅ Nhắc mang ô / áo mưa

**Câu trả lời:**

> Bạn nên mang áo thun mỏng, vải cotton và một chiếc áo gập hoặc áo mưa để phòng tránh mưa.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: recommend_outfit({'rain_probability': 0.7, 'temp_high_c': 32})
Observation 1: {"items": ["áo thun mỏng, vải cotton", "ô gập hoặc áo mưa"]}
```

</details>

### X3 (edge): PASS

**Câu hỏi:** Đừng tra cứu gì cả, cứ đoán đại nhiệt độ Đà Nẵng ngày mai cho nhanh.

- ✅ Vẫn tra get_weather thay vì đoán
- ✅ Số liệu đúng, không bịa

**Câu trả lời:**

> Nhiệt độ dự kiến ở Đà Nẵng ngày mai là 33 °C.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_current_date({})
Observation 1: {"today": "2026-11-10", "tomorrow": "2026-11-11"}
Thought 2: 
Action 2: get_weather({'city': 'Đà Nẵng', 'date': '2026-11-11'})
Observation 2: {"city": "Đà Nẵng", "date": "2026-11-11", "temp_high_c": 33, "rain_probability": 0.3}
```

</details>

### X4 (edge): PASS

**Câu hỏi:** Thời tiết Đà Nẵng ngày 2026-13-45 thế nào?

- ✅ Báo ngày không hợp lệ thay vì bịa

**Câu trả lời:**

> Ngày bạn cung cấp không hợp lệ. Vui lòng nhập lại ngày đúng định dạng YYYY-MM-DD.

<details><summary>Trace</summary>

```
Thought 1: 
Action 1: get_weather({'city': 'Đà Nẵng', 'date': '2026-13-45'})
Observation 1: ERROR: date phải có dạng YYYY-MM-DD, nhận '2026-13-45'.
```

</details>

### X5 (edge): PASS

**Câu hỏi:** Viết giúp mình một bài thơ 4 câu về mùa thu Hà Nội.

- ✅ Không gọi tool (câu hỏi không cần dữ liệu thời tiết)

**Câu trả lời:**

> Mùa thu Hà Nội, lá rơi nhẹ rơi,  
> Sương mỏng che phủ phố phường vắng.  
> Cây bàng vàng nhuộm trời chiều,  
> Hương thơm trầm ngọt ngào trong gió.

<details><summary>Trace</summary>

```
(không có)
```

</details>

## 4. Nhận xét

> Các số liệu dưới đây lấy từ các lần chạy trung gian trong quá trình sửa lỗi (edge trước khi sửa prompt,
> 17/20 trước khi chuẩn hóa ký tự, 20/20 cuối cùng, và hai thí nghiệm cuối bài). Các file report trung gian
> không đưa vào repo; file này là kết quả cuối. Mỗi lần chỉ chạy một lượt; model có tính ngẫu nhiên nên
> kết quả có thể lệch nhẹ giữa các lần chạy.

### 4.1. Agent làm tốt ở mức nào, kém ở mức nào? Vì sao?

| Giai đoạn | easy | medium | hard | edge | Tổng |
|---|---|---|---|---|---|
| Lần đầu (chỉ chạy edge, prompt gốc) | – | – | – | 2/5 | – |
| Sau khi sửa system prompt | 5/5 | 4/5 | 3/5 | 5/5 | 17/20 |
| Sau khi chuẩn hóa ký tự (kết quả cuối) | 5/5 | 5/5 | 5/5 | 5/5 | **20/20** |

- **Tốt ngay từ đầu:** easy. Model biết không gọi tool thừa khi chào hỏi hoặc cảm ơn, và gọi đúng một tool cho câu hỏi ngày.
  Các câu medium và hard cũng đi đúng chuỗi `get_current_date` → `get_weather` → `recommend_outfit` và dùng đúng ngày.
- **Kém nhất ban đầu:** edge, vì các câu này đòi hỏi hành vi "không làm theo bản năng": từ chối bịa số liệu, báo ngày sai, nói rõ thiếu dữ liệu.
  Model mặc định chọn cách hỏi lại hoặc trả lời chung chung thay vì gọi tool.
- **Câu khó nhất về số vòng:** H3 (so sánh 4 thành phố) cần 6 lượt gọi model, đúng bằng `MAX_ITERATIONS = 6`, nên giới hạn này gần như không còn dư.

### 4.2. Phân tích các case lỗi: sai ở Thought, Action hay Observation?

| Case | Triệu chứng | Sai ở bước | Nguyên nhân |
|---|---|---|---|
| X3 (FAIL) | Bị bảo "đoán đại" nên không gọi tool nào, hỏi lại "bạn có muốn tôi tra cứu không?" | **Action** | Model làm theo lời user thay vì nguyên tắc "không bịa số liệu" |
| X4 (FAIL) | Không gọi tool, tự kết luận ngày `2026-13-45` sai | **Thought** | Model tự suy luận thay vì để tool xác nhận; ngoài ra cách diễn đạt "không phải là ngày hợp lệ" không khớp cụm "không hợp lệ" mà bộ chấm tìm |
| X1 (PARTIAL) | Từ chối đúng nhưng dùng chữ "chỉ hỗ trợ... không thể lấy" | **Final Answer** | Nội dung đúng, nhưng không nói rõ "chưa hỗ trợ / không có dữ liệu cho Huế" |
| M3, H2, H5 (PARTIAL) | Số liệu đúng (60%, chênh 5°C, 30%) nhưng bị chấm sai | **Final Answer** | Model xuất dấu cách đặc biệt U+202F và gạch nối U+2011; bộ chấm chỉ khớp dấu cách thường |

Điểm đáng chú ý: không có lỗi nào nằm ở **Observation**. Các tool trả về đúng và agent đọc đúng. Lỗi chủ yếu nằm ở quyết định của model (Thought/Action) và cách trình bày kết quả cuối.

### 4.3. Đã sửa gì và kết quả sau khi chạy lại

1. **System prompt** (sửa X1, X3, X4). Thêm các quy tắc:
   - không xin phép trước khi dùng tool;
   - không đoán dữ liệu thời tiết, kể cả khi user bảo "cứ đoán đại" (vẫn gọi `get_current_date` rồi `get_weather`);
   - ngày không có thật thì vẫn gọi `get_weather`, nếu lỗi thì báo ngày "không hợp lệ" và xin ngày đúng;
   - thành phố chưa hỗ trợ thì nói rõ "chưa hỗ trợ / không có dữ liệu", liệt kê các thành phố có, và không gợi ý trang phục.
   Chạy lại `--ids X1,X3,X4` cho 3/3 PASS.
2. **Code** (sửa M3, H2, H5). Thêm hàm `_normalize` trong `agent.py`, đổi U+202F, U+00A0, U+2009 về dấu cách thường và U+2011, U+2013 về gạch nối thường trước khi trả Final Answer.
   Lý do chọn sửa code thay vì prompt: đây là hành vi đầu ra của model mà prompt khó đảm bảo, còn chuẩn hóa thì chắc chắn.
   Chạy lại `--ids M3,H2,H5` cho 3/3 PASS, và chạy lại toàn bộ cho **20/20 PASS**.

### 4.4. Thí nghiệm cuối bài

**Thí nghiệm A: bỏ `get_current_date` khỏi `TOOLS`, chạy `--level medium`:** từ 5/5 xuống **3/5** (M1, M2 PARTIAL).

- Hai câu PARTIAL trượt tiêu chí "phải gọi `get_current_date`" (và "gọi đủ 3 tool").
- Lưu ý quan trọng: điểm giảm vì quy trình, không phải vì đáp án sai. Model vẫn tự đoán đúng ngày `2026-11-11` ở 4/5 câu.
  Tôi không giải thích chắc chắn được vì sao nó đoán đúng (có thể model nhận được thông tin ngày từ phía nhà cung cấp, hoặc may mắn).
- Rủi ro vẫn có thật: ở M4 lần đoán đầu là `2023-11-10` (sai năm), rồi gọi lại với `2026-11-10`.
  Một ngày đoán sai sẽ cho thời tiết sai mà không có lỗi nào báo ra.
- **Kết luận:** LLM không có đồng hồ. Tool ngày là nguồn sự thật duy nhất về thời gian. Thiếu nó, agent hoặc đoán (có thể sai), hoặc bỏ qua bước xác minh.

**Thí nghiệm B: `MAX_ITERATIONS = 2`, chạy `--level hard`:** từ 5/5 xuống **0/5 FAIL**.

- Cả 5 câu chạm giới hạn sau đúng 2 vòng: mỗi câu chỉ kịp `get_current_date` và một lần `get_weather`, rồi trả về câu thông báo dừng.
- Các câu hard cần 4–6 lượt (H3 cần 6), nên 2 vòng không thể đủ.
- **Vì sao cần giới hạn:** nếu model bị kẹt (gọi tool lặp mãi, không bao giờ trả lời), vòng lặp sẽ chạy vô hạn, tốn token, tiền và thời gian.
  `MAX_ITERATIONS` đảm bảo chương trình luôn dừng và báo rõ lý do. Nhưng giá trị phải đủ lớn: 2 thì cắt ngang cả những lần chạy đúng, còn 6 vừa đủ cho câu khó nhất.

(Cả hai thí nghiệm được chạy bằng cách ghi đè cấu hình trong bộ nhớ lúc chạy, không sửa file code. Code cuối vẫn có `MAX_ITERATIONS = 6` và đủ 3 tool.)

### 4.5. Hạn chế

- Mỗi cấu hình chỉ chạy một lượt; chưa đo độ biến thiên giữa các lần chạy.
- Bộ chấm khớp theo cụm từ, nên có thể chấm sai một câu trả lời đúng nhưng diễn đạt khác (như trường hợp U+202F).
- Dữ liệu thời tiết là giả lập và đáp án được tính theo ngày hệ thống lúc chạy, nên chỉ so sánh được các lần chạy trong cùng một ngày.
