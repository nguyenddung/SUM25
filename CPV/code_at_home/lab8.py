import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Tạo model Eigenfaces
recognizer = cv2.face.EigenFaceRecognizer_create()


def train_model():
    labels = []
    faces = []
    label_dict = {}
    cur_label = 0
    for root, dirs, files in os.walk("dataset"):
        for name in files:
            if name.endswith("jpg") or name.endswith("png"):
                path = os.path.join(root, name)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                faces.append(cv2.resize(img, (200, 200)))
                person_name = os.path.basename(root)
                if person_name not in label_dict:
                    label_dict[person_name] = cur_label
                    cur_label += 1
                labels.append(label_dict[person_name])
    recognizer.train(faces, np.array(labels))
    return label_dict


label_map = train_model()


# GUI
class FaceRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Recognition with Eigenfaces")
        self.image_path = None

        self.label = Label(
            master, text="Face Recognition with Eigenfaces", font=("Arial", 16)
        )
        self.label.pack(pady=10)

        self.canvas = Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.btn_select = Button(master, text="Chọn ảnh", command=self.select_image)
        self.btn_select.pack(pady=5)

        self.btn_recognize = Button(
            master, text="Nhận diện khuôn mặt", command=self.recognize_face
        )
        self.btn_recognize.pack(pady=5)

    def select_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image_path = path
            img = Image.open(path)
            img = img.resize((400, 400))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.tk_img)

    def recognize_face(self):
        if not self.image_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn ảnh trước.")
            return
        img = cv2.imread(self.image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            messagebox.showinfo("Thông báo", "Không tìm thấy khuôn mặt nào.")
            return

        for x, y, w, h in faces:
            face_roi = gray[y : y + h, x : x + w]
            face_resized = cv2.resize(face_roi, (200, 200))
            label, confidence = recognizer.predict(face_resized)
            name = [k for k, v in label_map.items() if v == label][0]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                img,
                f"{name} ({confidence:.2f})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )

        # Hiển thị ảnh kết quả
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb).resize((400, 400))
        self.tk_img = ImageTk.PhotoImage(img_pil)
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_img)


# Chạy chương trình
if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
