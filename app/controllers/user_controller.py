from math import ceil
from fastapi import APIRouter, Depends, Query, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_role
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.core.database import get_db1_session

router = APIRouter(dependencies=[Depends(require_role("admin"))])


@router.get("/")
async def get_users(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Количество записей на странице")
):
    service = UserService(db)
    skip = (page - 1) * page_size
    users, total_users = await service.get_users(skip, page_size)
    total_pages = ceil(total_users / page_size)
    return {
        "users": users,
        "page": page,
        "page_size": page_size,
        "total_users": total_users,
        "total_pages": total_pages
    }


@router.get("/{user_id}")
async def get_user(
    user_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.get_user(user_id)


@router.post("/")
async def create_user(
    user_data: UserCreate = Body(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.create_user(user_data)


@router.put("/{user_id}")
async def update_user(
    user_data: UserUpdate = Body(...),
    user_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.update_user(user_id, user_data)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = UserService(db)
    return await service.delete_user(user_id)
