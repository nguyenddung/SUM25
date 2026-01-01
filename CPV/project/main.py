import cv2
import tkinter as tk
from database import Database
from face_recognition import FaceRecognition
from attendance import Attendance
from email_notification import EmailNotification
from gui import GUI


def main():
    # Thông tin kết nối cơ sở dữ liệu
    server = "AUSTINNGUYEN"  # Tên máy chủ SQL Server của bạn
    database = "AttendanceDB"  # Đổi thành tên cơ sở dữ liệu thực tế của bạn

    # Kết nối cơ sở dữ liệu
    db = Database(server, database)

    # Khởi tạo nhận diện khuôn mặt
    face_recognition_system = FaceRecognition(db)

    # Khởi tạo hệ thống điểm danh
    attendance_system = Attendance(db, face_recognition_system)

    # Khởi tạo giao diện người dùng
    root = tk.Tk()
    gui = GUI(root, attendance_system, face_recognition_system, db)
    root.mainloop()


if __name__ == "__main__":
    main()
