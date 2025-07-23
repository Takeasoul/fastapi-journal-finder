from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.security import require_role
from app.schemas.oecd import OECDCreate, OECDUpdate, OECDOut
from app.core.database import get_db1_session
from app.services.oecd_service import (
    get_all_oecd,
    get_oecd_by_id,
    create_oecd,
    update_oecd,
    delete_oecd
)

router = APIRouter()

@router.get(
    "/",
    response_model=List[OECDOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех элементов OECD",
    description="Этот эндпоинт возвращает список всех элементов OECD из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_oecd(db: AsyncSession = Depends(get_db1_session)):
    return await get_all_oecd(db)

@router.get(
    "/{oecd_id}",
    response_model=OECDOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить элемент OECD по ID",
    description="Этот эндпоинт возвращает информацию об элементе OECD по указанному ID. "
                "Если элемент не найден, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_oecd(oecd_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    oecd = await get_oecd_by_id(db, oecd_id)
    if not oecd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OECD не найден")
    return oecd

@router.post(
    "/",
    response_model=OECDOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новый элемент OECD",
    description="Этот эндпоинт создает новую запись элемента OECD в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_oecd_item(data: OECDCreate, db: AsyncSession = Depends(get_db1_session)):
    return await create_oecd(db, data)

@router.put(
    "/{oecd_id}",
    response_model=OECDOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить элемент OECD",
    description="Этот эндпоинт обновляет информацию об элементе OECD по указанному ID. "
                "Если элемент не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_oecd_item(oecd_id: int, data: OECDUpdate, db: AsyncSession = Depends(get_db1_session)):
    oecd = await update_oecd(db, oecd_id, data)
    if not oecd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OECD не найден")
    return oecd

@router.delete(
    "/{oecd_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить элемент OECD",
    description="Этот эндпоинт удаляет элемент OECD по указанному ID. "
                "Если элемент не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_oecd_item(oecd_id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await delete_oecd(db, oecd_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OECD не найден")
    return {"detail": "OECD удален"}