class EmailTemplates:
    @staticmethod
    def confirmation_email_template(confirmation_link: str) -> str:
        return f"""
        <html>
          <body>
            <p>Здравствуйте!</p>
            <p>Для завершения регистрации на сайте перейдите по ссылке ниже:</p>
            <a href="{confirmation_link}">Подтвердить аккаунт</a>
            <p>Если вы не регистрировались на нашем сайте, проигнорируйте это письмо.</p>
            <p>С уважением,<br>Команда yourdomain.com</p>
          </body>
        </html>
        """

    @staticmethod
    def password_reset_email_template(reset_link: str) -> str:
        return f"""
        <html>
          <body>
            <p>Здравствуйте!</p>
            <p>Для сброса пароля перейдите по ссылке ниже:</p>
            <a href="{reset_link}">Сбросить пароль</a>
            <p>Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
            <p>С уважением,<br>Команда yourdomain.com</p>
          </body>
        </html>
        """