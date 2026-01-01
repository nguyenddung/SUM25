import face_recognition


class Attendance:
    def __init__(self, student_images):
        self.student_images = student_images

    def mark_attendance(self, frame):
        rgb_frame = frame[:, :, ::-1]  # Chuyển từ BGR sang RGB
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        attendance = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                list(self.student_images.values()), face_encoding
            )
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = list(self.student_images.keys())[first_match_index]
            attendance.append(name)
        return attendance
