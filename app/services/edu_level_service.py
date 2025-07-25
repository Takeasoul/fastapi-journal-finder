from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from starlette import status

from app.models.edu_level import EduLevel
from app.schemas.edu_level import EduLevelCreate, EduLevelUpdate


async def get_all_edu_levels(db: AsyncSession):
    try:
        result = await db.execute(select(EduLevel))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении уровней образования")


async def get_edu_level_by_id(db: AsyncSession, edu_level_id: int):
    try:
        result = await db.execute(select(EduLevel).where(EduLevel.id == edu_level_id))
        edu_level = result.scalar_one_or_none()
        if not edu_level:
            raise HTTPException(status_code=404, detail="Уровень образования не найден")
        return edu_level
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении уровня образования")


async def create_edu_level(db: AsyncSession, data: EduLevelCreate):
    try:
        edu_level = EduLevel(**data.dict())
        db.add(edu_level)
        await db.commit()
        await db.refresh(edu_level)
        return edu_level
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при создании уровня образования")


async def update_edu_level(db: AsyncSession, edu_level_id: int, data: EduLevelUpdate):
    try:
        edu_level = await get_edu_level_by_id(db, edu_level_id)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(edu_level, field, value)
        await db.commit()
        await db.refresh(edu_level)
        return edu_level
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при обновлении уровня образования")


async def delete_edu_level(db: AsyncSession, edu_level_id: int):
    try:
        edu_level = await get_edu_level_by_id(db, edu_level_id)
        if not edu_level:
            return False
        await db.delete(edu_level)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при удалении уровня образования")
