from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.role import RoleResponse  # Абсолютный импорт

class UserCreate(BaseModel):
    username: EmailStr
    password: str
    ip: Optional[str]
    role_id: int

class UserUpdate(BaseModel):
    username: Optional[EmailStr]
    password: Optional[str]
    ip: Optional[str]
    role_id: Optional[int]
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    username: EmailStr
    ip: Optional[str]
    role: RoleResponse

    class Config:
        from_attributes = True
