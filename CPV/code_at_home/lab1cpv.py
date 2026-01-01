import cv2
import numpy as np
import math

# Kích thước canvas
width, height = 800, 800
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255


# Vẽ lưới tọa độ lên canvas
def draw_grid(img, spacing=50, color=(200, 200, 200)):
    h, w = img.shape[:2]
    for x in range(0, w, spacing):
        cv2.line(img, (x, 0), (x, h), color, 1)
    for y in range(0, h, spacing):
        cv2.line(img, (0, y), (w, y), color, 1)


# draw_grid(canvas)

# Biến toàn cục
original_rectangle = []
transformed_rectangle = []
drawing = False
p1, p2 = (-1, -1), (-1, -1)


# Hàm vẽ hình chữ nhật
def draw_rectangle(img, pt1, pt2, color=(0, 0, 255)):
    cv2.rectangle(img, pt1, pt2, color, 2)


# Hàm xử lý sự kiện chuột
def mouse_callback(event, x, y, flags, param):
    global p1, p2, drawing, original_rectangle, canvas

    temp_canvas = canvas.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        p1 = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        p2 = (x, y)
        draw_rectangle(temp_canvas, p1, p2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        p2 = (x, y)
        draw_rectangle(canvas, p1, p2)
        original_rectangle = [p1, (p2[0], p1[1]), p2, (p1[0], p2[1])]

    cv2.imshow("Canvas", temp_canvas)


# Áp dụng biến đổi lên các điểm
def apply_transformation(matrix, points):
    result = []
    for pt in points:
        vec = np.array([pt[0], pt[1], 1])
        transformed = matrix @ vec
        result.append((int(transformed[0]), int(transformed[1])))
    return result


# Vẽ hình chữ nhật sau biến đổi
def draw_transformed(rect, color=(0, 255, 0)):
    for i in range(4):
        cv2.line(canvas, rect[i], rect[(i + 1) % 4], color, 2)


# Tịnh tiến
def translation(tx, ty):
    M = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    return M


# Xoay quanh tâm
def rotation(angle_deg, center):
    angle = math.radians(angle_deg)
    cx, cy = center  # day la cai tuple xiu truyen tham so vao
    T1 = translation(-cx, -cy)
    R = np.array(
        [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1],
        ]
    )
    T2 = translation(cx, cy)
    return T2 @ R @ T1


# Co dãn quanh tâm
def scaling(sx, sy, center):
    cx, cy = center
    T1 = translation(-cx, -cy)
    S = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
    T2 = translation(cx, cy)
    return T2 @ S @ T1


# Tạo cửa sổ và callback chuột
cv2.namedWindow("Canvas")
cv2.setMouseCallback("Canvas", mouse_callback)

# Vòng lặp chính
while True:
    cv2.imshow("Canvas", canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):  # Quit
        break
    elif key == ord("t") and original_rectangle:
        tx = int(input("Nhập giá trị tịnh tiến theo x: "))
        ty = int(input("Nhập giá trị tịnh tiến theo y: "))
        M = translation(tx, ty)
        transformed_rectangle = apply_transformation(M, original_rectangle)
        draw_transformed(transformed_rectangle, color=(0, 255, 0))

    elif key == ord("r") and original_rectangle:
        angle = float(input("Nhập góc quay (độ): "))
        cx = (p1[0] + p2[0]) // 2  # tâm của hcn
        cy = (p1[1] + p2[1]) // 2
        M = rotation(angle, (cx, cy))
        transformed_rectangle = apply_transformation(M, original_rectangle)
        draw_transformed(transformed_rectangle, color=(255, 0, 0))

    elif key == ord("s") and original_rectangle:
        sx = float(input("Nhập hệ số scale theo x: "))
        sy = float(input("Nhập hệ số scale theo y: "))
        cx = (p1[0] + p2[0]) // 2
        cy = (p1[1] + p2[1]) // 2
        M = scaling(sx, sy, (cx, cy))
        transformed_rectangle = apply_transformation(M, original_rectangle)
        draw_transformed(transformed_rectangle, color=(0, 0, 255))

    elif key == ord("c"):
        canvas = np.ones((height, width, 3), dtype=np.uint8) * 255
        original_rectangle = []
        transformed_rectangle = []
        p1, p2 = (-1, -1), (-1, -1)
cv2.destroyAllWindows()
