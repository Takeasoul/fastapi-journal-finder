from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.role import RoleResponse  # Абсолютный импорт

class UserCreate(BaseModel):
    username: EmailStr
    password: str
    ip: Optional[str] = None
    role_id: int
    is_active: Optional[bool] = None

class UserUpdate(BaseModel):
    username: Optional[EmailStr] = None
    password: Optional[str] = None
    ip: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    username: EmailStr = None
    ip: Optional[str] = None
    role: RoleResponse = None

    class Config:
        from_attributes = True
