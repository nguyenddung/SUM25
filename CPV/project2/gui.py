import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


class GUI:
    def __init__(self, face_recognition, db):
        self.face_recognition = face_recognition
        self.db = db
        self.window = tk.Tk()
        self.window.title("Hệ thống điểm danh sinh viên")

    def add_student_ui(self):
        # Giao diện thêm sinh viên
        def add_student():
            name = entry_name.get()
            image_path = filedialog.askopenfilename()
            if name and image_path:
                self.face_recognition.add_student(name, image_path)
                messagebox.showinfo("Thông báo", "Thêm sinh viên thành công!")
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin.")

        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10)

        label_name = tk.Label(frame, text="Tên sinh viên:")
        label_name.grid(row=0, column=0, pady=5)

        entry_name = tk.Entry(frame)
        entry_name.grid(row=0, column=1, pady=5)

        button_add = tk.Button(frame, text="Thêm sinh viên", command=add_student)
        button_add.grid(row=1, columnspan=2, pady=10)

    def delete_student_ui(self):
        # Giao diện xóa sinh viên
        def delete_student():
            student_id = entry_id.get()
            if student_id:
                self.db.delete_student(student_id)
                messagebox.showinfo("Thông báo", "Xóa sinh viên thành công!")
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID sinh viên.")

        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10)

        label_id = tk.Label(frame, text="ID sinh viên:")
        label_id.grid(row=0, column=0, pady=5)

        entry_id = tk.Entry(frame)
        entry_id.grid(row=0, column=1, pady=5)

        button_delete = tk.Button(frame, text="Xóa sinh viên", command=delete_student)
        button_delete.grid(row=1, columnspan=2, pady=10)

    def show_attendance_ui(self):
        # Giao diện điểm danh sinh viên
        self.face_recognition.recognize_face()

    def show_absent_students(self):
        # Hiển thị sinh viên vắng
        absent_students = self.db.get_absent_students()
        message = "Sinh viên vắng mặt:\n" + "\n".join(
            [student[1] for student in absent_students]
        )
        messagebox.showinfo("Sinh viên vắng", message)

    def run(self):
        # Giao diện chính
        button_add_student = tk.Button(
            self.window, text="Thêm sinh viên", command=self.add_student_ui
        )
        button_add_student.pack(pady=10)

        button_delete_student = tk.Button(
            self.window, text="Xóa sinh viên", command=self.delete_student_ui
        )
        button_delete_student.pack(pady=10)

        button_show_attendance = tk.Button(
            self.window, text="Điểm danh", command=self.show_attendance_ui
        )
        button_show_attendance.pack(pady=10)

        button_show_absent = tk.Button(
            self.window, text="Sinh viên vắng", command=self.show_absent_students
        )
        button_show_absent.pack(pady=10)

        self.window.mainloop()
