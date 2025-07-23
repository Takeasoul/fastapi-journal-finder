import uuid

from cryptography.fernet import Fernet
from sqlalchemy import ForeignKey, Column, UUID, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE

from app.core.base import Base
from app.core.config import settings

cipher = Fernet(settings.ENCRYPTION_KEY)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    ip = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=False)
    confirmation_token = Column(String(255), nullable=True)  # Токен для подтверждения
    reset_password_token = Column(String(255), nullable=True)  # Токен для сброса пароля
    reset_password_token_expires = Column(DateTime(timezone=True), nullable=True)  # Время истечения токена сброса

    role = relationship("Role", back_populates="users")