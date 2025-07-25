from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import require_role
from app.schemas.role import RoleRequest
from app.services.role_service import RoleService
from app.core.database import get_db1_session

router = APIRouter(dependencies=[Depends(require_role("admin"))])


@router.post(
    "/",
    description="Создает новую роль. Доступно только администраторам."
)
async def create_role(
    data: RoleRequest,
    db: AsyncSession = Depends(get_db1_session)
):
    service = RoleService(db)
    return await service.create_role(data)


@router.get(
    "/",
    description="Получает список всех ролей. Доступно только администраторам."
)
async def get_roles(db: AsyncSession = Depends(get_db1_session)):
    service = RoleService(db)
    return await service.get_roles()


@router.put(
    "/{role_id}",
    description="Обновляет название роли по её ID. Доступно только администраторам."
)
async def update_role(
    data: RoleRequest,
    role_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = RoleService(db)
    return await service.update_role(role_id, data)


@router.delete(
    "/{role_id}",
    description="Удаляет роль по её ID. Доступно только администраторам."
)
async def delete_role(
    role_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = RoleService(db)
    return await service.delete_role(role_id)
