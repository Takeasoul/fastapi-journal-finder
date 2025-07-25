from math import ceil
from typing import Optional

from fastapi import APIRouter, Depends, Query, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_role
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.core.database import get_db1_session

router = APIRouter(dependencies=[Depends(require_role("admin"))])


@router.get(
    "/",
    description="Получает список всех пользователей с поддержкой пагинации и фильтрации. "
                "- **page**: Номер страницы (начинается с 1). "
                "- **page_size**: Количество записей на странице (максимум 100). "
                "- **username**: Фильтр по имени пользователя (email). "
                "- **role_id**: Фильтр по ID роли. "
                "- **is_active**: Фильтр по состоянию активации (True/False). "
                "Доступно только администраторам."
)
async def get_users(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Количество записей на странице"),
    username: Optional[str] = Query(None, description="Фильтр по имени пользователя (email)"),
    role_id: Optional[int] = Query(None, description="Фильтр по ID роли"),
    is_active: Optional[bool] = Query(None, description="Фильтр по состоянию активации")
):
    service = UserService(db)
    skip = (page - 1) * page_size
    users, total_users = await service.get_users_filtered(skip, page_size, username=username, role_id=role_id, is_active=is_active)
    total_pages = ceil(total_users / page_size)
    return {
        "users": users,
        "page": page,
        "page_size": page_size,
        "total_users": total_users,
        "total_pages": total_pages
    }


@router.get(
    "/{user_id}",
    description="Получает пользователя по его ID. Если пользователь не найден, возвращается ошибка 404. "
                "Доступно только администраторам."
)
async def get_user(
    user_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.get_user(user_id)


@router.post(
    "/",
    description="Создает нового пользователя. Доступно только администраторам."
)
async def create_user(
    user_data: UserCreate = Body(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.create_user(user_data)


@router.put(
    "/{user_id}",
    description="Обновляет информацию о пользователе по его ID. Если пользователь не найден, возвращается ошибка 404. "
                "Доступно только администраторам."
)
async def update_user(
    user_data: UserUpdate = Body(...),
    user_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    description="Удаляет пользователя по его ID. Если пользователь не найден, возвращается ошибка 404. "
                "Доступно только администраторам."
)
async def delete_user(
    user_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.delete_user(user_id)


@router.post(
    "/activate",
    summary="Активация аккаунта по ID или email",
    description="Этот эндпоинт активирует аккаунт пользователя по его ID или email."
)
async def activate_account(
    user_id: int = None,
    email: str = None,
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.activate_user(user_id=user_id, email=email)