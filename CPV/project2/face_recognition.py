import cv2
import dlib
import numpy as np
from student import Student
from email_notification import send_email


class FaceRecognition:
    def __init__(self, db):
        self.db = db
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.facerec = dlib.face_recognition_model_v1(
            "dlib_face_recognition_resnet_model_v1.dat"
        )

    def add_student(self, student_name, image_path):
        # Nhận diện gương mặt và mã hóa
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if len(faces) > 0:
            # Lấy gương mặt đầu tiên
            face = faces[0]
            shape = self.sp(gray, face)
            face_encoding = np.array(self.facerec.compute_face_descriptor(img, shape))

            # Lưu sinh viên vào cơ sở dữ liệu
            self.db.add_student(student_name, face_encoding.tobytes())

    def recognize_face(self):
        # Mở webcam và nhận diện gương mặt
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)

            for face in faces:
                shape = self.sp(gray, face)
                face_encoding = np.array(
                    self.facerec.compute_face_descriptor(frame, shape)
                )

                # So khớp với sinh viên trong cơ sở dữ liệu
                for student in self.db.get_all_students():
                    student_encoding = np.frombuffer(
                        student.face_encoding, dtype=np.float64
                    )

                    # So sánh độ tương đồng (sử dụng hàm cosine hoặc Euclidean distance)
                    distance = np.linalg.norm(face_encoding - student_encoding)

                    if distance < 0.6:
                        status = "Có mặt"
                        self.db.add_attendance(student.student_id, status)
                        cv2.putText(
                            frame,
                            f"{student.name}: {status}",
                            (face.left(), face.top() - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 0, 0),
                            2,
                        )
                        break

            cv2.imshow("Face Attendance System", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
