import cv2

# Tải mô hình Haar Cascade để phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Mở camera (hoặc tải video)
cap = cv2.VideoCapture(
    0
)  # 0 là ID của camera mặc định. Bạn có thể thay bằng đường dẫn video.

while True:
    # Đọc frame từ camera
    ret, frame = cap.read()

    # Chuyển ảnh sang ảnh đen trắng để xử lý nhanh hơn
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt trong ảnh
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Vẽ hình chữ nhật quanh các khuôn mặt phát hiện được
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Hiển thị ảnh với các khuôn mặt được đánh dấu
    cv2.imshow("Face Detection", frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Giải phóng camera và đóng tất cả cửa sổ
cap.release()
cv2.destroyAllWindows()
