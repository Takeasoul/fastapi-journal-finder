from pydantic import BaseModel
from typing import Optional
from app.schemas.role import RoleResponse  # Абсолютный импорт

class UserCreate(BaseModel):
    username: str
    password: str
    ip: Optional[str]
    role_id: int

class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    ip: Optional[str]
    role_id: Optional[int]

class UserResponse(BaseModel):
    id: int
    username: str
    ip: Optional[str]
    role: RoleResponse

    class Config:
        from_attributes = True
