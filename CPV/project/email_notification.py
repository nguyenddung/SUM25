import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotification:
    def __init__(self, smtp_server, port, login, password):
        self.smtp_server = smtp_server
        self.port = port
        self.login = login
        self.password = password

    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.login
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.login, self.password)
            text = msg.as_string()
            server.sendmail(self.login, to_email, text)
