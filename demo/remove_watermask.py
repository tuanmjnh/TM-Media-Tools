# pip install opencv-python numpy
import cv2
import numpy as np

# Đọc ảnh ban đầu
image = cv2.imread("input/image.png")

# Lấy kích thước ảnh
height, width = image.shape[:2]

# Tạo mask cho khu vực watermark "MINIMAX" (góc dưới bên phải)
mask = np.zeros((height, width), dtype=np.uint8)

# Xác định khu vực watermark
# Dựa trên ảnh, watermark chiếm khoảng 150 pixel từ dưới và 200 pixel từ phải
text_height = 80
text_width = 320
mask[height - text_height:height, width - text_width:width] = 255

# Áp dụng inpainting để tái tạo khu vực
inpainted_image = cv2.inpaint(image, mask, inpaintRadius=20, flags=cv2.INPAINT_TELEA)

# Lưu ảnh kết quả
cv2.imwrite("output/image_no_watermark.jpg", inpainted_image)
