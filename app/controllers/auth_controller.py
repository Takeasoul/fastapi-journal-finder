from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin, urlencode

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db1_session
from app.core.logger import logger
from app.core.security import require_role, generate_reset_password_token, get_password_hash, \
    get_reset_password_token_expiry
from app.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, ChangeUserRoleRequest, RefreshTokenRequest
from app.services.auth_service import AuthService
from app.services.email_service import EmailService

router = APIRouter()


@router.post(
    "/register",
    response_model=dict,
    summary="Регистрация нового пользователя",
    description="Этот эндпоинт регистрирует нового пользователя в системе. "
                "Пользователь должен предоставить данные для регистрации, такие как имя пользователя и пароль. "
                "Если регистрация успешна, возвращается сообщение об успехе."
)
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


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Вход пользователя в систему",
    description="Этот эндпоинт позволяет пользователю войти в систему. "
                "Пользователь должен предоставить имя пользователя и пароль. "
                "Если аутентификация успешна, возвращаются токены JWT."
)
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

@router.post(
    "/swagger-login",
    summary="Вход для Swagger UI (OAuth2 form)",
    description="Этот эндпоинт используется для входа через форму Swagger UI. "
                "Он принимает имя пользователя и пароль через форму и возвращает токены JWT.",
    tags=["auth"]
)
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

router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Обновление токенов",
    description="Этот эндпоинт обновляет JWT-токены доступа и обновления на основе предоставленного refresh-токена. "
                "Если refresh-токен действителен, возвращаются новые токены."
)
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


@router.put(
    "/change-role",
    dependencies=[Depends(require_role("admin"))],
    summary="Изменение роли пользователя",
    description="Этот эндпоинт позволяет администратору изменить роль указанного пользователя. "
                "Требуется роль 'admin' для выполнения этого действия. "
                "Возвращает сообщение об успешном изменении роли."
)
async def change_user_role(
    data: ChangeUserRoleRequest,
    db: AsyncSession = Depends(get_db1_session)
) -> dict:
    service = AuthService(db)
    result = await service.change_user_role(data.user_id, data.new_role)
    logger.info(f"Смена роли для пользователя {data.user_id} на {data.new_role}")
    return {
        "message": "Роль успешно изменена",
        "user_id": data.user_id,
        "new_role": data.new_role
    }


@router.post(
    "/confirm",
    summary="Подтверждение аккаунта",
    description="Этот эндпоинт активирует аккаунт пользователя по токену подтверждения."
)
async def confirm_account(
    token: str,
    db: AsyncSession = Depends(get_db1_session)
):
    result = await db.execute(select(User).where(User.confirmation_token == token))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Неправильный или истекший токен подтверждения")

    # Активация аккаунта
    user.is_active = True
    user.confirmation_token = None  # Очищаем токен после использования
    await db.commit()

    return {"message": "Аккаунт успешно подтвержден"}

@router.post(
    "/request-password-reset",
    summary="Запрос кода для сброса пароля",
    description="Этот эндпоинт отправляет код для сброса пароля на указанный email."
)
async def request_password_reset(
    email: str,
    db: AsyncSession = Depends(get_db1_session)
):
    result = await db.execute(select(User).where(User.username == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Юзер не найден")

    # Генерация токена сброса пароля
    reset_token = generate_reset_password_token()
    user.reset_password_token = reset_token
    user.reset_password_token_expires = get_reset_password_token_expiry()
    await db.commit()

    # Отправка письма с инструкциями
    base_url = f"http://localhost:5173/auth?mode=reset-password"
    query_params = {"token": reset_token}

    reset_link = base_url + "?" + urlencode(query_params)
    await EmailService().send_email(
        recipient_email=email,
        subject="Сброс пароля",
        body=f"Нажмите на ссылку для сброса пароля: {reset_link}"
    )

    return {"message": "Инструкции по смене пароля отправлены на почту"}

@router.post(
    "/reset-password",
    name="reset_password_endpoint",
    summary="Сброс пароля",
    description="Этот эндпоинт позволяет сбросить пароль с использованием токена."
)
async def reset_password(
    token: str,
    new_password: str,
    db: AsyncSession = Depends(get_db1_session)
):
    result = await db.execute(select(User).where(User.reset_password_token == token))
    user = result.scalar_one_or_none()
    # Определяем текущее время в UTC
    now_utc = datetime.now(timezone.utc)

    # Преобразуем offset-naive datetime в offset-aware, если необходимо
    if user and user.reset_password_token_expires.tzinfo is None:
        user.reset_password_token_expires = user.reset_password_token_expires.replace(tzinfo=timezone.utc)

    # Проверяем, существует ли пользователь и не истек ли токен
    if not user or user.reset_password_token_expires < now_utc:
        raise HTTPException(status_code=400, detail="Неправильный или истекший токен смены пароля")

    # Обновление пароля
    user.password = get_password_hash(new_password)
    user.reset_password_token = None
    user.reset_password_token_expires = None
    await db.commit()

    return {"message": "Пароль успешно сменен"}

@router.post(
    "/resend-confirmation",
    summary="Повторная отправка письма с подтверждением аккаунта",
    description="Этот эндпоинт позволяет отправить письмо с подтверждением аккаунта повторно. "
                "Требуется указать email пользователя."
)
async def resend_confirmation(
    email: str,
    request: Request,
    db: AsyncSession = Depends(get_db1_session)
):
    try:
        service = AuthService(db)
        result = await service.resend_confirmation_email(email, request)
        logger.info(f"Resent confirmation email to: {email}")
        return result
    except HTTPException as e:
        logger.error(f"Resend confirmation failed: {e.detail}")
        raise e

