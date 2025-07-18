from fastapi import HTTPException, Request
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.logger import logger
from app.models.role import Role
from jose import JWTError, ExpiredSignatureError

from app.services.utils.ip_utils import is_ip_whitelisted


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, data: RegisterRequest, request: Request) -> dict:
        client_ip = request.headers.get("x-forwarded-for", request.client.host)

        # Определяем, нужно ли назначить роль user
        is_allowed = await is_ip_whitelisted(self.db, client_ip)
        role_name = "user" if is_allowed else "guest"

        role_query = await self.db.execute(select(Role).where(Role.name == role_name))
        role = role_query.scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=500, detail=f"Default role '{role_name}' not found")

        hashed_password = get_password_hash(data.password)

        new_user = User(
            username=data.username,
            password=hashed_password,
            ip=client_ip,
            role_id=role.id
        )
        self.db.add(new_user)
        await self.db.commit()

        logger.info(f"New user registered: {data.username} (IP: {client_ip}, Role: {role.name})")
        return {"message": "User registered successfully"}

    async def login_user(self, data: LoginRequest, request: Request) -> TokenResponse:
        user_query = await self.db.execute(select(User).where(User.username == data.username))
        user = user_query.scalar_one_or_none()
        if not user:
            logger.error(f"Login failed: User '{data.username}' not found")
            raise HTTPException(status_code=400, detail="Invalid username or password")

        logger.debug(f"Verifying password. Plain: {data.password}, Hashed: {user.password}")
        if not verify_password(data.password, user.password):
            logger.error(f"Password verification failed for user: {data.username}")
            raise HTTPException(status_code=400, detail="Invalid username or password")

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
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            # Проверяем существование пользователя
            user_query = await self.db.execute(select(User).where(User.username == username))
            user = user_query.scalar_one_or_none()
            if not user:
                logger.error(f"User not found for refresh token: {username}")
                raise HTTPException(status_code=401, detail="User not found")

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
            raise HTTPException(status_code=401, detail="Refresh token has expired")
        except JWTError as e:
            logger.error(f"JWT error during token refresh: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def change_user_role(self, user_id: int, new_role_id: int) -> dict:
        # Проверяем существование пользователя
        user_query = await self.db.execute(select(User).where(User.id == user_id))
        user = user_query.scalar_one_or_none()
        if not user:
            logger.error(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")

        # Проверяем существование роли
        role_query = await self.db.execute(select(Role).where(Role.id == new_role_id))
        role = role_query.scalar_one_or_none()
        if not role:
            logger.error(f"Role with ID {new_role_id} not found")
            raise HTTPException(status_code=404, detail="Role not found")

        # Обновляем роль пользователя
        user.role_id = new_role_id
        await self.db.commit()

        logger.info(f"Role for user {user_id} changed to {new_role_id}")
        return {"message": "Role updated successfully", "user_id": str(user_id), "new_role_id": str(new_role_id)}