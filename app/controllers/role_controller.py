from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import require_role
from app.services.role_service import RoleService
from app.core.database import get_db1_session

router = APIRouter(dependencies=[Depends(require_role("admin"))])


@router.post("/")
async def create_role(
    name: str = Body(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = RoleService(db)
    return await service.create_role(name)


@router.get("/")
async def get_roles(db: AsyncSession = Depends(get_db1_session)):
    service = RoleService(db)
    return await service.get_roles()


@router.put("/{role_id}")
async def update_role(
    role_id: int = Path(...),
    name: str = Body(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = RoleService(db)
    return await service.update_role(role_id, name)


@router.delete("/{role_id}")
async def delete_role(
    role_id: int = Path(...),
    db: AsyncSession = Depends(get_db1_session)
):
    service = RoleService(db)
    return await service.delete_role(role_id)
