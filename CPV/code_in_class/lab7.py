import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Tải bộ phân loại Haar Cascade để phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# Hàm chọn hình ảnh từ máy tính
def select_image():
    file_path = filedialog.askopenfilename()  # Mở cửa sổ chọn file
    if file_path:
        detect_faces(file_path)  # Gọi hàm phát hiện khuôn mặt


# Hàm phát hiện khuôn mặt trong ảnh
def detect_faces(image_path):
    # Đọc hình ảnh từ đường dẫn file
    img = cv2.imread(image_path)

    # Kiểm tra nếu ảnh không đọc được
    if img is None:
        print("Không thể đọc ảnh.")
        return

    # Chuyển đổi ảnh màu sang ảnh xám (grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt trong ảnh xám
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50)
    )

    # In số lượng khuôn mặt phát hiện
    print(f"Số lượng khuôn mặt phát hiện: {len(faces)}")

    # Kiểm tra nếu phát hiện được khuôn mặt
    if len(faces) == 0:
        print("Không phát hiện khuôn mặt.")

    # Vẽ hình chữ nhật quanh khuôn mặt đã phát hiện
    for x, y, w, h in faces:
        cv2.rectangle(
            img, (x, y), (x + w, y + h), (0, 255, 0), 3
        )  # Màu xanh lá và độ dày là 3

    # Chuyển đổi ảnh từ BGR sang RGB (Tkinter yêu cầu RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Chuyển đổi ảnh từ array sang định dạng PIL để sử dụng trong Tkinter
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Hiển thị ảnh trên giao diện Tkinter
    label.config(image=img_tk)
    label.image = img_tk  # Giữ ảnh trong bộ nhớ để tránh việc mất ảnh khi cập nhật


# Thiết lập cửa sổ giao diện đồ họa với Tkinter
root = tk.Tk()
root.title("Face Detection Application")

# Tạo một label để hiển thị ảnh
label = tk.Label(root)
label.pack()

# Tạo nút chọn hình ảnh
button = tk.Button(root, text="Select Image", command=select_image)
button.pack()

# Chạy vòng lặp sự kiện của Tkinter để giao diện hoạt động
root.mainloop()
