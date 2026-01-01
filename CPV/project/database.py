import pyodbc
import numpy as np


class Database:
    def __init__(self, server, database):
        self.connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;",
            autocommit=True,
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def insert_student(self, name, email, face_encoding):
        query = "INSERT INTO students (name, email, face_encoding) VALUES (?, ?, ?)"
        self.cursor.execute(
            query, (name, email, face_encoding.tobytes())
        )  # Lưu dưới dạng nhị phân
        self.connection.commit()

    def get_students(self):
        self.cursor.execute("SELECT id, name, email, face_encoding FROM students")
        return self.cursor.fetchall()

    def get_student_face_encoding(self, student_id):
        self.cursor.execute(
            "SELECT face_encoding FROM students WHERE id=?", (student_id,)
        )
        result = self.cursor.fetchone()
        if result:
            return np.frombuffer(
                result[0], dtype=np.float64
            )  # Chuyển lại thành numpy array
        return None
