import face_recognition
import numpy as np


class FaceRecognition:
    def __init__(self, db):
        self.db = db
        self.known_face_encodings = []
        self.known_face_ids = []
        self.load_known_faces()

    def load_known_faces(self):
        students = self.db.fetch_all("SELECT id, face_encoding FROM students")
        for student in students:
            student_id = student[0]
            face_encoding = np.frombuffer(student[1], dtype=np.float64)
            self.known_face_ids.append(student_id)
            self.known_face_encodings.append(face_encoding)

    def add_student_face(self, face_encoding):
        self.known_face_encodings.append(face_encoding)

    def recognize_face(self, frame):
        rgb_frame = frame[:, :, ::-1]  # Convert to RGB
        face_locations = face_recognition.face_locations(rgb_frame)

        if not face_locations:
            return []  # No face detected, return empty list

        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        recognized_students = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding
            )
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding
            )

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                recognized_students.append(self.known_face_ids[best_match_index])

        return recognized_students
