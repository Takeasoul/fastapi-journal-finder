from fastapi import APIRouter, Depends, Path, status, HTTPException
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_role
from app.models.pub_information import PubInformation
from app.schemas.pub_information import PubInformationOut, PubInformationCreate, PubInformationUpdate
from app.core.database import get_db1_session
from app.services.pub_information_service import (
    get_pub_info, create_pub_info, update_pub_info, delete_pub_info
)

router = APIRouter()

@router.get(
    "/",
    response_model=List[PubInformationOut],
    dependencies=[Depends(require_role("user"))],
    description="Получает список всей информации о публикациях. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_pub_infos(db: AsyncSession = Depends(get_db1_session)):
    # Опционально реализовать: получить все записи (если нужно)
    # Или убрать если не нужно
    result = await db.execute(select(PubInformation))
    return result.scalars().all()

@router.get(
    "/{pub_id}",
    response_model=PubInformationOut,
    dependencies=[Depends(require_role("user"))],
    description="Получает информацию о публикации по её ID. "
                "Если информация не найдена, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_pub_information(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    pub_info = await get_pub_info(db, pub_id)
    if not pub_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Информация о публикации не найдена")
    return pub_info

@router.post(
    "/",
    response_model=PubInformationOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
    description="Создает новую запись информации о публикации. "
                "Доступ разрешен только администраторам."
)
async def create_pub_information(data: PubInformationCreate, db: AsyncSession = Depends(get_db1_session)):
    return await create_pub_info(db, data)

@router.put(
    "/{pub_id}",
    response_model=PubInformationOut,
    dependencies=[Depends(require_role("admin"))],
    description="Обновляет информацию о публикации по её ID. "
                "Если информация не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_pub_information(pub_id: int, data: PubInformationUpdate, db: AsyncSession = Depends(get_db1_session)):
    updated_pub_info = await update_pub_info(db, pub_id, data)
    if not updated_pub_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Информация о публикации не найдена")
    return updated_pub_info

@router.delete(
    "/{pub_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("admin"))],
    description="Удаляет информацию о публикации по её ID. "
                "Если информация не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_pub_information(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await delete_pub_info(db, pub_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Информация о публикации не найдена")
