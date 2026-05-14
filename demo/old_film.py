import cv2
import numpy as np
import random
from tqdm import tqdm


# Đọc video đầu vào
input_video_path = "inputs/video.mp4"  # Thay bằng đường dẫn video của bạn
output_video_path = "outputs/video.mp4"


# Hàm áp dụng hiệu ứng phim cũ với hiệu ứng rách xé và phân hủy

def apply_old_film_effect(frame, frame_count, height, width):
    # 1. Grain/Noise
    noise = np.random.normal(0, 15, frame.shape)  # Increased noise for texture
    frame = cv2.convertScaleAbs(frame + noise)

    # 2. Sepia Tone (lightened for worn look)
    sepia_filter = np.array([[0.3, 0.6, 0.1],
                             [0.4, 0.7, 0.2],
                             [0.4, 0.8, 0.2]])
    frame = cv2.transform(frame, sepia_filter)
    frame = np.clip(frame, 0, 255)

    # 3. Vertical Scratches (enhanced frequency and length)
    if random.random() < 0.1:  # 10% chance per frame
        num_scratches = random.randint(1, 4)  # 1-4 scratches per frame
        for _ in range(num_scratches):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            length = random.randint(50, height)  # Longer scratches
            cv2.line(frame, (x, y), (x, min(y + length, height - 1)), (255, 255, 255), 1)

    # 4. Dust and Spots (increased frequency and size)
    if random.random() < 0.2:  # 20% chance per frame
        num_spots = random.randint(2, 8)  # 2-8 spots per frame
        for _ in range(num_spots):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            size = random.randint(1, 5)  # Larger spots
            cv2.circle(frame, (x, y), size, (255, 255, 255), -1)

    # 5. Flicker
    flicker_intensity = random.uniform(0.85, 1.15)  # Wider flicker range
    frame = np.clip(frame * flicker_intensity, 0, 255).astype(np.uint8)

    # 6. Vignette
    vignette = np.ones((height, width), dtype=np.uint8) * 255
    cv2.circle(vignette, (width // 2, height // 2), min(width, height) // 2, 0, -1)
    vignette = cv2.GaussianBlur(vignette, (0, 0), sigmaX=50)
    vignette = cv2.cvtColor(vignette, cv2.COLOR_GRAY2BGR)
    frame = cv2.addWeighted(frame, 0.8, vignette, 0.2, 0.0)

    # 7. Screen Tearing Effect
    if random.random() < 0.03:  # 3% chance per frame for tearing
        num_tears = random.randint(1, 2)  # 1-2 tears per frame
        for _ in range(num_tears):
            tear_y = random.randint(0, height - 1)
            tear_height = random.randint(20, 50)
            tear_shift = random.randint(-30, 30)

            start_y = max(0, tear_y)
            end_y = min(height, tear_y + tear_height)
            tear_slice = frame[start_y:end_y, :].copy()

            if tear_shift > 0:
                frame[start_y:end_y, tear_shift:width] = tear_slice[:, :width - tear_shift]
                frame[start_y:end_y, :tear_shift] = tear_slice[:, width - tear_shift:]
            elif tear_shift < 0:
                tear_shift = abs(tear_shift)
                frame[start_y:end_y, :width - tear_shift] = tear_slice[:, tear_shift:]
                frame[start_y:end_y, width - tear_shift:] = tear_slice[:, :tear_shift]

    return frame



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

# Xử lý từng khung hình với thanh tiến trình
print("Đang xử lý video...")
frame_count = 0
with tqdm(total=total_frames, desc="Tiến trình", unit="frame") as pbar:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Áp dụng hiệu ứng phim cũ
        frame = apply_old_film_effect(frame, frame_count, height, width)

        # Ghi khung hình vào video đầu ra
        out.write(frame)

        # Cập nhật thanh tiến trình
        frame_count += 1
        pbar.update(1)

# Giải phóng tài nguyên
cap.release()
out.release()
print("Video đã được xử lý và lưu tại:", output_video_path)
