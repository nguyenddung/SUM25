class Student:
    def __init__(self, student_id, name, face_encoding):
        self.student_id = student_id
        self.name = name
        self.face_encoding = face_encoding

    def __str__(self):
        return f"Student {self.name}, ID: {self.student_id}"
