import logging
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.database import get_db1_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/swagger-login")

logger = logging.getLogger(__name__)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__default_rounds=12
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db1_session)]
):
    from app.models.user import User
    from app.models.role import Role
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        result = await db.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(Role.parent)
            )
            .where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# Зависимость-проверка на наличие роли
def require_role(required_role: str):
    from app.models.user import User
    async def role_checker(
            current_user: Annotated[User, Depends(get_current_user)]
    ):
        # Проверка по иерархии
        if not await has_role(current_user.role, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
    return role_checker

async def has_role(user_role, required_role_name: str):
    current = user_role
    while current:
        if current.name == required_role_name:
            return True
        current = current.parent  # parent должен быть загружен (selectinload)
    return False

def get_password_hash(password: str) -> str:
    hashed = pwd_context.hash(password)
    logger.debug(f"Generated hash for password: {hashed}")
    return hashed


def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_valid = pwd_context.verify(plain_password, hashed_password)
    logger.debug(f"Password verification result: {is_valid}")
    return is_valid


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str, token_type: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")