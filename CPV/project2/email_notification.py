import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(absent_students):
    sender_email = "your_email@gmail.com"
    receiver_email = "instructor_email@gmail.com"
    password = "your_email_password"

    subject = "Danh sách sinh viên vắng học"
    body = "Danh sách sinh viên vắng học: " + ", ".join(
        [student.name for student in absent_students]
    )

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.close()
        print("Email đã được gửi thành công.")
    except Exception as e:
        print(f"Không thể gửi email: {e}")
