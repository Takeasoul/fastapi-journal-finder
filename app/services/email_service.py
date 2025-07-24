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

    async def send_email(self, recipient_email: str, subject: str, body: str, html_body: str = None):
        try:
            # Создание сообщения
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email

            # Добавление текстового содержимого
            text_part = MIMEText(body, "plain")
            message.attach(text_part)

            # HTML-версия письма (если передана)
            if html_body:
                html_part = MIMEText(html_body, "html")
                message.attach(html_part)

            # Отправка письма через SMTP
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email}")
        except smtplib.SMTPAuthenticationError:
            print("Ошибка аутентификации. Проверьте логин и пароль.")
        except smtplib.SMTPException as e:
            print(f"SMTP error: {e}")
        except Exception as e:
            print(f"Failed to send email: {e}")