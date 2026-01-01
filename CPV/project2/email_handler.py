import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    def __init__(self, smtp_server, from_email, password):
        self.smtp_server = smtp_server
        self.from_email = from_email
        self.password = password

    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, 587)
            server.starttls()
            server.login(self.from_email, self.password)
            server.sendmail(self.from_email, to_email, msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")
