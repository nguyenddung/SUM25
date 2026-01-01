import pyodbc


class Database:
    def __init__(self):
        self.connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=AUSTINNGUYEN;"
            "DATABASE=StudentDB;"
            "Trusted_Connection=yes;",
            autocommit=True,
        )
        self.cursor = self.connection.cursor()

    def add_student(self, name, face_encoding):
        sql = "INSERT INTO Students (name, face_encoding) VALUES (?, ?)"
        self.cursor.execute(sql, (name, face_encoding))
        self.connection.commit()

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM Students")
        return self.cursor.fetchall()

    def delete_student(self, student_id):
        sql = "DELETE FROM Students WHERE student_id = ?"
        self.cursor.execute(sql, (student_id,))
        self.connection.commit()

    def add_attendance(self, student_id, status):
        sql = "INSERT INTO Attendance (student_id, status) VALUES (?, ?)"
        self.cursor.execute(sql, (student_id, status))
        self.connection.commit()

    def get_absent_students(self):
        self.cursor.execute("SELECT * FROM Students WHERE status = 'Vắng'")
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()
