import uuid

from cryptography.fernet import Fernet
from sqlalchemy import ForeignKey, Column, UUID, String, Integer
from sqlalchemy.orm import relationship

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

    role = relationship("Role", back_populates="users")