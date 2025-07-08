from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db1_session
from app.core.logger import logger
from app.core.security import require_role
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, ChangeUserRoleRequest, RefreshTokenRequest
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=dict)
async def register_user(
    data: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db1_session)
) -> dict:
    try:
        service = AuthService(db)
        result = await service.register_user(data, request)
        logger.info(f"User registered: {data.username}")
        return result
    except HTTPException as e:
        logger.error(f"Registration failed: {e.detail}")
        raise e


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db1_session)
) -> TokenResponse:
    try:
        service = AuthService(db)
        result = await service.login_user(data, request)
        logger.info(f"User logged in: {data.username}")
        return result
    except HTTPException as e:
        logger.error(f"Login failed: {e.detail}")
        raise e

@router.post("/swagger-login", summary="Login for Swagger UI (OAuth2 form)", tags=["auth"])
async def swagger_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db1_session)
):
    from app.services.auth_service import AuthService
    from app.schemas.auth import LoginRequest
    service = AuthService(db)
    data = LoginRequest(username=username, password=password)
    token = await service.login_user(data, request)
    return token

@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db1_session)
) -> TokenResponse:
    try:
        service = AuthService(db)
        result = await service.refresh_tokens(data.refresh_token)
        logger.info("Tokens refreshed successfully")
        return result
    except HTTPException as e:
        logger.error(f"Token refresh failed: {e.detail}")
        raise e


@router.put("/change-role", dependencies=[Depends(require_role("admin"))])
async def change_user_role(
    data: ChangeUserRoleRequest,
    db: AsyncSession = Depends(get_db1_session)
) -> dict:
    service = AuthService(db)
    result = await service.change_user_role(data.user_id, data.new_role)
    logger.info(f"Role changed for user {data.user_id} to {data.new_role}")
    return {
        "message": "Role updated successfully",
        "user_id": data.user_id,
        "new_role": data.new_role
    }
