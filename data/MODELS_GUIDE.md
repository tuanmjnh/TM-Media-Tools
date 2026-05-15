# Hướng dẫn chọn Model Gemini cho TM-Media-Tools

Tài liệu này tổng hợp danh sách các model Google Gemini khả dụng và mục đích sử dụng tối ưu cho từng loại.

## 1. Nhóm Model Đa Năng (Văn bản, Hình ảnh, Audio, Code)
Các model này thường được dùng để hiểu nội dung (Phân tích ảnh, tóm tắt, viết code).

| Tên Model | Đặc điểm | Phù hợp cho | Chi phí (Ước tính) |
| :--- | :--- | :--- | :--- |
| `gemini-2.0-flash` | Nhanh, thông minh, hỗ trợ đa phương thức. | Đa số các tác vụ phổ thông. | Rất rẻ ($) |
| `gemini-2.0-pro` | Thông minh nhất, xử lý logic cực tốt. | Lập trình, suy luận khó, phân tích sâu. | Trung bình ($$$) |
| `gemini-2.0-flash-lite` | Siêu nhanh, siêu rẻ. | Các tác vụ đơn giản, xử lý số lượng lớn. | Cực rẻ (Tiết kiệm nhất) |
| `gemini-2.5-flash` | Bản nâng cấp của 2.0 Flash. | Xử lý ảnh chi tiết hơn, ngữ cảnh lớn hơn. | Rất rẻ ($) |

---

## 2. Nhóm Model Chuyên Xử Lý & Xuất Hình Ảnh (Native Image)
Dành cho các tác vụ cần AI trả về kết quả là một file ảnh (Image-to-Image).

| Tên Model | Đặc điểm | Phù hợp cho | Chi phí (Ước tính) |
| :--- | :--- | :--- | :--- |
| `gemini-3.1-flash-image-preview` | Xuất ảnh trực tiếp (Native Output). | Tối ưu ảnh, sửa ảnh, thay đổi độ phân giải. | Cao ($$$) |
| `gemini-3-pro-image-preview` | Chất lượng ảnh cao cấp nhất. | Chỉnh sửa ảnh chuyên sâu, nghệ thuật. | Rất cao ($$$$) |
| `gemini-2.5-flash-image` | Ổn định, nhận diện thị giác tốt. | Phân tích và xử lý thị giác máy tính. | Trung bình ($$) |

---

## 3. Nhóm Model Tạo Ảnh & Video (Generative AI)
Dành cho việc tạo mới nội dung từ câu lệnh văn bản (Text-to-Image/Video).

| Tên Model | Đặc điểm | Phù hợp cho | Chi phí (Ước tính) |
| :--- | :--- | :--- | :--- |
| `imagen-4.0-generate-001` | Tạo ảnh từ văn bản chất lượng cao. | Vẽ tranh AI, tạo concept art, minh họa. | ~$0.03 - $0.05 / ảnh |
| `imagen-4.0-ultra-generate-001` | Đỉnh cao về độ chi tiết và nghệ thuật. | Các yêu cầu tạo ảnh cực khó, độ phân giải cao. | ~$0.08 - $0.12 / ảnh |
| `veo-3.1-generate-preview` | Tạo video ngắn từ văn bản/ảnh. | Làm clip ngắn, motion graphics bằng AI. | ~$0.10 / giây video |

---

## 5. Các Gói Cước Chính (Tùy thuộc vào Google Cloud Project)

### Gói Miễn Phí (Free Tier)
- **Chi phí:** $0 (Yêu cầu bật Google AI Studio).
- **Hạn mức:** Khoảng 15 yêu cầu/phút (cho bản Flash) và giới hạn tổng số yêu cầu mỗi ngày.
- **Quyền riêng tư:** Dữ liệu có thể được Google dùng để huấn luyện model.

### Gói Trả Phí (Pay-as-you-go)
- **Chi phí:** Tính trên số lượng Token đầu vào/đầu ra hoặc số lượng ảnh/giây video tạo ra.
- **Ưu điểm:** Hạn mức cao hơn rất nhiều, không bị giới hạn tốc độ gắt gao.
- **Quyền riêng tư:** Dữ liệu của bạn được bảo mật và không dùng để huấn luyện model.

---

## Cách sử dụng:
Để thay đổi model cho ứng dụng, bạn chỉ cần mở file `.env` và cập nhật dòng:
```env
DEFAULT_MODEL=tên_model_muốn_dùng
```
Sau đó khởi động lại ứng dụng.
