from datetime import datetime


class Attendance:
    def __init__(self, db_connection, face_recognition_system):
        self.db = db_connection
        self.face_recognition_system = face_recognition_system

    def mark_attendance(self, frame):
        recognized_students = self.face_recognition_system.recognize_face(frame)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for student_id in recognized_students:
            self.db.insert_attendance(student_id, timestamp)

    def get_attendance(self):
        self.db.cursor.execute(
            """
            SELECT students.name, attendance.timestamp FROM attendance
            JOIN students ON attendance.student_id = students.id
        """
        )
        return self.db.cursor.fetchall()
