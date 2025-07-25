from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from app.models.index import Index
from app.schemas.index import IndexCreate, IndexUpdate

async def get_all_indexes(db: AsyncSession):
    try:
        result = await db.execute(select(Index))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении списка индексаций")

async def get_index_by_pub_id(db: AsyncSession, pub_id: int):
    try:
        result = await db.execute(select(Index).where(Index.pub_id == pub_id))
        idx = result.scalar_one_or_none()
        if not idx:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Индексация не найдена")
        return idx
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении индексации")

async def create_index(db: AsyncSession, data: IndexCreate):
    try:
        idx = Index(**data.dict())
        db.add(idx)
        await db.commit()
        await db.refresh(idx)
        return idx
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при создании индексации")

async def update_index(db: AsyncSession, pub_id: int, data: IndexUpdate):
    try:
        idx = await get_index_by_pub_id(db, pub_id)
        if idx:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(idx, key, value)
            await db.commit()
            await db.refresh(idx)
        return idx
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при обновлении индексации")

async def delete_index(db: AsyncSession, pub_id: int):
    try:
        idx = await get_index_by_pub_id(db, pub_id)
        if idx:
            await db.delete(idx)
            await db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Индексация не найдена")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при удалении индексации")
