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
- **min_image_duration / max_image_duration**: Khoảng thời gian hiển thị 1 ảnh (giây), hỗ trợ số thập phân.
- **min_transition_duration / max_transition_duration**: Khoảng thời gian của hiệu ứng chuyển cảnh (giây), hỗ trợ số thập phân.
- **default_fps**: Khung hình trên giây (VD: `30`, `60`).
- **transitions**: Danh sách các hiệu ứng muốn dùng. Để trống `[]` sẽ dùng ngẫu nhiên từ `data/transitions.txt`.
- **codec_id**: ID bộ mã hóa video (VD: `libx264` cho mp4). Xem `data/encodings.json`.
- **resolution_id**: ID độ phân giải (VD: `h-fhd` cho 1080p ngang). Xem `data/resolutions.json`.
- **ffmpeg_binary**: Đường dẫn file `ffmpeg.exe`. Nếu để trống sẽ tự tìm trong `bin/ffmpeg/`.

## 3. Đường dẫn (`paths`)
- **input_dir**: Thư mục chứa ảnh đầu vào. Hỗ trợ đường dẫn tuyệt đối (VD: `C:/Images`) hoặc tương đối (VD: `input`).
- **output_dir**: Thư mục lưu kết quả. Hỗ trợ đường dẫn tuyệt đối hoặc tương đối.

## 4. Thử lại (`retry`)
- **delay**: Thời gian chờ giữa các lần thử (giây).
+
+## 5. Lệnh Hệ thống (`System`)
+- **Khôi phục cấu hình**: Nếu file `config.json` bị lỗi hoặc bạn muốn quay lại thiết lập ban đầu, hãy chọn mục **7** trong menu chính.
- **Tự động tạo cấu hình**: Nếu file `config.json` bị xóa, ứng dụng sẽ tự động tạo lại file này từ bản mẫu trong thư mục `data/default_config.json`.
