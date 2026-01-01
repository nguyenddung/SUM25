class Student:
    def __init__(self, student_id, name, email, face_encoding):
        self.student_id = student_id  # ID sinh viên trong cơ sở dữ liệu
        self.name = name  # Tên sinh viên
        self.email = email  # Email sinh viên
        self.face_encoding = face_encoding  # Khuôn mặt (face encoding) của sinh viên

    def __repr__(self):
        return f"Student(id={self.student_id}, name={self.name}, email={self.email})"
