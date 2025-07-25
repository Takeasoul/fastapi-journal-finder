from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from app.models.grnti import Grnti
from app.schemas.grnti import GrntiCreate, GrntiUpdate

async def get_all_grnti(db: AsyncSession):
    try:
        result = await db.execute(select(Grnti))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении записей ГРНТИ")

async def get_grnti_by_id(db: AsyncSession, grnti_id: int):
    try:
        result = await db.execute(select(Grnti).where(Grnti.id == grnti_id))
        grnti = result.scalar_one_or_none()
        if not grnti:
            raise HTTPException(status_code=404, detail="ГРНТИ не найден")
        return grnti
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении записи ГРНТИ")

async def create_grnti(db: AsyncSession, data: GrntiCreate):
    try:
        grnti = Grnti(**data.dict())
        db.add(grnti)
        await db.commit()
        await db.refresh(grnti)
        return grnti
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при создании записи ГРНТИ")

async def update_grnti(db: AsyncSession, grnti_id: int, data: GrntiUpdate):
    try:
        grnti = await get_grnti_by_id(db, grnti_id)
        if grnti:
            for field, value in data.dict(exclude_unset=True).items():
                setattr(grnti, field, value)
            await db.commit()
            await db.refresh(grnti)
        return grnti
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при обновлении записи ГРНТИ")

async def delete_grnti(db: AsyncSession, grnti_id: int):
    try:
        grnti = await get_grnti_by_id(db, grnti_id)
        if not grnti:
            return False
        await db.delete(grnti)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при удалении записи ГРНТИ")
