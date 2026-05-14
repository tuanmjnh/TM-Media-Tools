import cv2
import numpy as np
import random
from tqdm import tqdm

# Đọc video đầu vào
input_video_path = "inputs/video.mp4"  # Thay bằng đường dẫn video của bạn
output_video_path = "outputs/video.mp4"


# Lớp để quản lý một ánh sao

class Sparkle:
    def __init__(self, x, y, max_radius=10, max_brightness=255, lifespan=30):
        self.x = x
        self.y = y
        self.max_radius = max_radius  # Maximum length of beams
        self.max_brightness = max_brightness
        self.lifespan = lifespan  # Số khung hình ánh sao tồn tại
        self.age = 0  # Tuổi hiện tại của ánh sao
        self.radius = 0  # Kích thước ban đầu của beams
        self.brightness = 0  # Độ sáng ban đầu

    def update(self):
        self.age += 1
        # Tính tỷ lệ tiến trình của chu kỳ sống (0 -> 1)
        progress = self.age / self.lifespan
        if progress < 0.5:
            # Nửa đầu: lớn dần và sáng lên
            self.radius = self.max_radius * (progress / 0.5)
            self.brightness = self.max_brightness * (progress / 0.5)
        else:
            # Nửa sau: giữ kích thước, giảm độ sáng
            self.radius = self.max_radius
            self.brightness = self.max_brightness * (1 - (progress - 0.5) / 0.5)
        return self.age <= self.lifespan

    def draw(self, frame):
        if self.brightness <= 0:
            return

        # Tạo một lớp phủ riêng để vẽ ánh sao
        overlay = np.zeros_like(frame, dtype=np.uint8)
        brightness = int(self.brightness)
        thickness = max(1, int(self.radius / 5))  # Độ dày của tia sáng

        # Vẽ 4 tia sáng chính (hình chữ thập)
        length = int(self.radius)
        cv2.line(overlay, (int(self.x - length), int(self.y)), (int(self.x + length), int(self.y)),
                 (brightness, brightness, brightness), thickness)
        cv2.line(overlay, (int(self.x), int(self.y - length)), (int(self.x), int(self.y + length)),
                 (brightness, brightness, brightness), thickness)

        # Vẽ 4 tia sáng phụ (chéo)
        length_diag = int(length / 1.414)  # Độ dài tia chéo (1/sqrt(2))
        cv2.line(overlay, (int(self.x - length_diag), int(self.y - length_diag)),
                 (int(self.x + length_diag), int(self.y + length_diag)),
                 (brightness, brightness, brightness), thickness)
        cv2.line(overlay, (int(self.x - length_diag), int(self.y + length_diag)),
                 (int(self.x + length_diag), int(self.y - length_diag)),
                 (brightness, brightness, brightness), thickness)

        # Tạo hiệu ứng tỏa sáng bằng Gaussian blur
        overlay = cv2.GaussianBlur(overlay, (9, 9), 0)

        # Kết hợp lớp phủ với khung hình
        frame[...] = cv2.add(frame, overlay)

# Hàm tạo hiệu ứng ánh sao lấp lánh


def add_sparkle_effect(frame, sparkles, spawn_probability=0.02, width=1920, height=1080):
    sparkle_frame = frame.copy()

    # Vẽ và cập nhật các ánh sao hiện có
    for sparkle in sparkles[:]:
        sparkle.draw(sparkle_frame)
        if not sparkle.update():
            sparkles.remove(sparkle)

    # Thêm ánh sao mới ngẫu nhiên dựa trên xác suất
    if random.random() < spawn_probability:
        num_new_sparkles = random.randint(1, 6)  # Số lượng ánh sao mới mỗi lần (1-3)
        for _ in range(num_new_sparkles):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            sparkles.append(Sparkle(x, y, max_radius=10, max_brightness=255, lifespan=30))

    # Kết hợp khung hình gốc và hiệu ứng để tạo độ trong suốt
    alpha = 0.5
    sparkle_frame = cv2.addWeighted(frame, 1 - alpha, sparkle_frame, alpha, 0.0)

    return sparkle_frame



cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    print("Không thể mở video!")
    exit()

# Lấy thông tin video
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Tạo video đầu ra
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Danh sách để lưu các ánh sao
sparkles = []

# Xử lý từng khung hình với thanh tiến trình
print("Đang xử lý video...")
with tqdm(total=total_frames, desc="Tiến trình", unit="frame") as pbar:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Áp dụng hiệu ứng ánh sao
        sparkle_frame = add_sparkle_effect(frame, sparkles, spawn_probability=0.02, width=width, height=height)

        # Ghi khung hình vào video đầu ra
        out.write(sparkle_frame)

        # Cập nhật thanh tiến trình
        pbar.update(1)

# Giải phóng tài nguyên
cap.release()
out.release()
print("Video đã được xử lý và lưu tại:", output_video_path)
