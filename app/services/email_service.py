import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.yandex.ru"
        self.smtp_port = 465  # SSL порт для почты
        self.sender_email = settings.EMAIL_SENDER
        self.sender_password = settings.EMAIL_PASSWORD

    async def send_email(self, recipient_email: str, subject: str, body: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = recipient_email

        # Добавляем текстовое содержимое письма
        text_part = MIMEText(body, "plain")
        message.attach(text_part)

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")