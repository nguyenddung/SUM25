from gui import GUI
from face_recognition import FaceRecognition
from database import Database


def main():
    # Khởi tạo kết nối với cơ sở dữ liệu
    db = Database()

    # Khởi tạo nhận diện gương mặt
    face_recognition = FaceRecognition(db)

    # Khởi tạo giao diện người dùng
    gui = GUI(face_recognition, db)

    gui.run()


if __name__ == "__main__":
    main()
