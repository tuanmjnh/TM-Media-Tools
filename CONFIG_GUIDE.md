# Hướng dẫn cấu hình TM Media Tools

File `config.json` chứa toàn bộ thiết lập cho các ứng dụng trong bộ công cụ. Dưới đây là giải thích chi tiết các thông số:

## 1. Gemini Image Optimizer (`gemini`)
- **api_key**: Khóa API Google Gemini của bạn.
- **model_name**: Tên model AI (VD: `gemini-1.5-flash-002`).
- **prompt**: Câu lệnh gửi cho AI để xử lý ảnh.

## 2. FFmpeg Video Creator (`video`)
- **image_formats**: Danh sách định dạng ảnh đầu vào (VD: `[".jpg", ".png"]`).
- **min_images / max_images**: Khoảng số lượng ảnh sẽ chọn ngẫu nhiên.
- **min_duration / max_duration**: Khoảng thời lượng video mong muốn (giây).
- **reuse_images**: `true` nếu cho phép dùng lại ảnh đã chọn, `false` nếu muốn ảnh duy nhất.
- **image_duration**: Thời gian hiển thị 1 ảnh (giây).
- **transition_duration**: Thời gian của hiệu ứng chuyển cảnh (giây).
- **default_fps**: Khung hình trên giây (VD: `30`, `60`).
- **transitions**: Danh sách các hiệu ứng muốn dùng. Để trống `[]` sẽ dùng ngẫu nhiên từ `data/transitions.txt`.
- **codec_id**: ID bộ mã hóa video (VD: `libx264` cho mp4). Xem `data/encodings.json`.
- **resolution_id**: ID độ phân giải (VD: `h-fhd` cho 1080p ngang). Xem `data/resolutions.json`.
- **ffmpeg_binary**: Đường dẫn file `ffmpeg.exe`. Nếu để trống sẽ tự tìm trong `bin/ffmpeg/`.

## 3. Đường dẫn (`paths`)
- **input_dir**: Thư mục chứa ảnh đầu vào.
- **output_dir**: Thư mục lưu kết quả.

## 4. Thử lại (`retry`)
- **count**: Số lần thử lại nếu lỗi API (Rate Limit).
- **delay**: Thời gian chờ giữa các lần thử (giây).
