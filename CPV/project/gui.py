import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageTk


class GUI:
    def __init__(self, root, attendance_system, face_recognition_system, db):
        self.root = root
        self.attendance_system = attendance_system
        self.face_recognition_system = face_recognition_system
        self.db = db
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Student Attendance System")

        self.video_source = 0  # Webcam
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        self.add_student_button = tk.Button(
            self.root, text="Add Student", command=self.add_student
        )
        self.add_student_button.pack(pady=10)

        self.mark_attendance_button = tk.Button(
            self.root, text="Mark Attendance", command=self.mark_attendance
        )
        self.mark_attendance_button.pack(pady=10)

        self.attendance_button = tk.Button(
            self.root, text="View Attendance", command=self.view_attendance
        )
        self.attendance_button.pack(pady=10)

        self.update_video()

    def update_video(self):
        ret, frame = self.vid.read()
        if ret:
            self.attendance_system.mark_attendance(frame)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=imgtk, anchor="nw")
            self.root.after(
                100, self.update_video
            )  # Reduce frame rate for better performance

    def add_student(self):
        name = "Student Name"  # You can prompt user for input
        email = "student@example.com"  # You can prompt user for input

        ret, frame = self.vid.read()
        if ret:
            face_encodings = face_recognition.face_encodings(frame)
            if face_encodings:
                face_encoding = face_encodings[0]
                self.db.insert_student(name, email, face_encoding)
                self.face_recognition_system.add_student_face(face_encoding)
                messagebox.showinfo("Success", "Student added successfully!")
            else:
                messagebox.showwarning(
                    "No Face Detected", "No face detected in the image."
                )

    def mark_attendance(self):
        messagebox.showinfo("Attendance", "Attendance has been marked.")

    def view_attendance(self):
        attendance = self.attendance_system.get_attendance()
        if isinstance(attendance, str):
            messagebox.showinfo("Attendance", attendance)
        else:
            for record in attendance:
                print(f"{record[0]} - {record[1]}")
