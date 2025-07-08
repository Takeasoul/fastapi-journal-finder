from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ChangeUserRoleRequest(BaseModel):
    user_id: int
    new_role: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str