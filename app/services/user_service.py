from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, generate_confirmation_token


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
        return user

    async def get_users(self, skip: int, limit: int) -> tuple[list[User], int]:
        total_users = await self.db.scalar(select(func.count()).select_from(User))
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        users = list(result.scalars().all())
        return users, total_users

    async def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            password=hashed_password,
            ip=user_data.ip,
            role_id=user_data.role_id,
            is_active=False,  # Новый пользователь неактивен до подтверждения
            confirmation_token=generate_confirmation_token()  # Генерация токена подтверждения
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user


    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_user(user_id)
        if user_data.username:
            user.username = user_data.username
        if user_data.password:
            user.password = get_password_hash(user_data.password)
        if user_data.ip is not None:
            user.ip = user_data.ip
        if user_data.role_id is not None:
            user.role_id = user_data.role_id
        if user_data.is_active is not None:
            user.is_active = user_data.is_active  # Обновление статуса активации
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> dict:
        user = await self.get_user(user_id)
        await self.db.delete(user)
        await self.db.commit()
        return {"message": "Пользователь удален успешно"}

    async def count_users(self) -> int:
        return await self.db.scalar(select(func.count()).select_from(User))

    async def activate_user_by_id(self, user_id: int) -> dict:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        if user.is_active:
            raise HTTPException(status_code=400, detail="Аккаунт пользователя уже активирован")

        # Активация аккаунта
        user.is_active = True
        user.confirmation_token = None  # Очищаем токен после использования
        await self.db.commit()
        return {"message": "Аккаунт подтвержден успешно"}

    async def activate_user(self, user_id: int = None, email: str = None) -> dict:
        if user_id is not None:
            # Активация по ID
            result = await self.db.execute(select(User).where(User.id == user_id))
        elif email is not None:
            # Активация по email
            result = await self.db.execute(select(User).where(User.username == email))
        else:
            raise HTTPException(status_code=400, detail="Необходимо указать либо идентификатор пользователя, либо адрес электронной почты")

        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        if user.is_active:
            raise HTTPException(status_code=400, detail="Аккаунт пользователя уже активирован")

        # Активация аккаунта
        user.is_active = True
        user.confirmation_token = None  # Очищаем токен после использования
        await self.db.commit()
        return {"message": "Аккаунт подтвержден успешно"}