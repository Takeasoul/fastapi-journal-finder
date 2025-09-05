import re

from fastapi import HTTPException, Request
from pydantic import validate_email
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, \
    decode_token, generate_confirmation_token
from app.core.logger import logger
from app.models.role import Role
from jose import JWTError, ExpiredSignatureError

from app.services.utils.email_templates import EmailTemplates
from app.services.utils.ip_utils import is_ip_whitelisted
from app.services.email_service import EmailService

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_service = EmailService()
    async def register_user(self, data: RegisterRequest, request: Request) -> dict:

        result = await self.db.execute(select(User).where(User.username == data.username))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Данный Email уже зарегистрирован")

        if not validate_email(data.username):
            raise HTTPException(status_code=400, detail="Введите валидный email")

        client_ip = request.headers.get("x-forwarded-for", request.client.host)

        # Определяем, нужно ли назначить роль user
        is_allowed = await is_ip_whitelisted(self.db, client_ip)
        role_name = "user" if is_allowed else "guest"

        role_query = await self.db.execute(select(Role).where(Role.name == role_name))
        role = role_query.scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=500, detail=f"Роль '{role_name}' не найдена")

        # Генерация токена подтверждения
        confirmation_token = generate_confirmation_token()

        # Формирование ссылки для подтверждения
        confirmation_link = f"https://330657.simplecloud.ru/auth?mode=confirm&token={confirmation_token}"

        # Получение HTML-шаблона письма
        html_body = EmailTemplates.confirmation_email_template(confirmation_link)

        try:
            # Попытка отправить письмо с подтверждением
            await self.email_service.send_email(
                recipient_email=data.username,
                subject="Подтверждение аккаунта",
                body=f"Пожалуйста подтвердите свой аккаунт перейдя по ссылке: {confirmation_link}",
                html_body=html_body
            )
        except Exception as e:
            # Если отправка письма не удалась, выбрасываем исключение
            logger.error(f"Ошибка отправки сообщения на почту: {e}")
            raise HTTPException(status_code=500, detail="Ошибка отправки сообщения на почту")


        hashed_password = get_password_hash(data.password)
        new_user = User(
            username=data.username,
            password=hashed_password,
            ip=request.client.host,
            role_id=role.id,
            is_active=False,  # Аккаунт неактивен до подтверждения
            confirmation_token=confirmation_token
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return {"message": "Пользователь успешно зарегистрирован. Пожалуйста подтвердите аккаунт при помощи ссылки на почте."}

    async def login_user(self, data: LoginRequest, request: Request) -> TokenResponse:
        user_query = await self.db.execute(select(User).where(User.username == data.username))
        user = user_query.scalar_one_or_none()
        if not user:
            logger.error(f"Ошибка авторизации: Пользователь '{data.username}' не найден")
            raise HTTPException(status_code=400, detail="Неправильный логин или пароль")

        logger.debug(f"Verifying password. Plain: {data.password}, Hashed: {user.password}")
        if not verify_password(data.password, user.password):
            logger.error(f"Password verification failed for user: {data.username}")
            raise HTTPException(status_code=400, detail="Неправильный логин или пароль")

        if not user.is_active:
            logger.error(f"Login failed: User '{data.username}' account is not activated")
            raise HTTPException(status_code=400, detail="Аккаунт не подтвержден. Пожалуйста подтвердите аккаунт при помощи ссылки на почте.")
        # Получение IP
        client_ip = request.headers.get("x-forwarded-for", request.client.host)
        logger.info(f"Login attempt from IP: {client_ip} for user: {data.username}")

        # Проверяем, входит ли IP в вайтлист
        is_allowed = await is_ip_whitelisted(self.db, client_ip)

        # Получаем текущую роль
        role_query = await self.db.execute(select(Role).where(Role.id == user.role_id))
        current_role = role_query.scalar_one_or_none()

        # Если IP в вайтлисте и текущая роль — guest, то обновим на user
        if is_allowed and current_role and current_role.name == "guest":
            new_role_query = await self.db.execute(select(Role).where(Role.name == "user"))
            new_role = new_role_query.scalar_one_or_none()
            if new_role:
                user.role_id = new_role.id
                await self.db.commit()
                logger.info(f"User '{user.username}' role upgraded from 'guest' to 'user' based on IP {client_ip}")

        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})
        logger.info(f"User logged in: {data.username}")

        return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        try:
            # Декодируем и проверяем refresh-токен
            payload = decode_token(refresh_token, token_type="refresh")
            username = payload.get("sub")
            if not username:
                logger.error("Invalid refresh token: missing 'sub'")
                raise HTTPException(status_code=401, detail="Неправильный refresh-токен")

            # Проверяем существование пользователя
            user_query = await self.db.execute(select(User).where(User.username == username))
            user = user_query.scalar_one_or_none()
            if not user:
                logger.error(f"User not found for refresh token: {username}")
                raise HTTPException(status_code=401, detail="Пользователь не найден")

            # Генерируем новые токены
            access_token = create_access_token(data={"sub": user.username})
            new_refresh_token = create_refresh_token(data={"sub": user.username})
            logger.info(f"Tokens refreshed successfully for user: {username}")

            return TokenResponse(
                access_token=access_token,
                refresh_token=new_refresh_token,
                token_type="bearer"
            )
        except ExpiredSignatureError:
            logger.error("Refresh token has expired")
            raise HTTPException(status_code=401, detail="Refresh-токен истек")
        except JWTError as e:
            logger.error(f"JWT error during token refresh: {str(e)}")
            raise HTTPException(status_code=401, detail="Неправильный refresh-токен")
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def change_user_role(self, user_id: int, new_role_id: int) -> dict:
        # Проверяем существование пользователя
        user_query = await self.db.execute(select(User).where(User.id == user_id))
        user = user_query.scalar_one_or_none()
        if not user:
            logger.error(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Проверяем существование роли
        role_query = await self.db.execute(select(Role).where(Role.id == new_role_id))
        role = role_query.scalar_one_or_none()
        if not role:
            logger.error(f"Role with ID {new_role_id} not found")
            raise HTTPException(status_code=404, detail="Роль не найдена")

        # Обновляем роль пользователя
        user.role_id = new_role_id
        await self.db.commit()

        logger.info(f"Role for user {user_id} changed to {new_role_id}")
        return {"message": "Role updated successfully", "user_id": str(user_id), "new_role_id": str(new_role_id)}

    async def resend_confirmation_email(self, email: str, request: Request) -> dict:
        # Поиск пользователя по email
        result = await self.db.execute(select(User).where(User.username == email))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь с таким email не найден")

        if user.is_active:
            raise HTTPException(status_code=400, detail="Аккаунт уже подтвержден")

        # Генерация нового токена подтверждения
        confirmation_token = generate_confirmation_token()
        confirmation_link = f"https://330657.simplecloud.ru/auth?mode=confirm&token={confirmation_token}"

        # Получение HTML-шаблона письма
        html_body = EmailTemplates.confirmation_email_template(confirmation_link)

        try:
            # Отправка письма с подтверждением
            await self.email_service.send_email(
                recipient_email=email,
                subject="Подтверждение аккаунта",
                body=f"Пожалуйста подтвердите свой аккаунт перейдя по ссылке: {confirmation_link}",
                html_body = html_body
            )
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения на почту: {e}")
            raise HTTPException(status_code=500, detail="Ошибка отправки сообщения на почту")

        # Обновление токена подтверждения в базе данных
        user.confirmation_token = confirmation_token
        await self.db.commit()
        await self.db.refresh(user)

        return {
            "message": "Письмо с подтверждением отправлено повторно. Пожалуйста подтвердите аккаунт при помощи ссылки на почте."}


    def validate_email(email: str) -> bool:
        # Регулярное выражение для базовой проверки формата email
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        # Проверка формата email
        if not re.match(email_regex, email):
            return False

        # Проверка допустимых доменов (.ru или .com)
        if not email.endswith(('.ru', '.com')):
            return False

        return True