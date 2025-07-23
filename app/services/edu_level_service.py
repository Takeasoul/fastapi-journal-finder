from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.edu_level import EduLevel
from app.schemas.edu_level import EduLevelCreate, EduLevelUpdate


async def get_all_edu_levels(db: AsyncSession):
    result = await db.execute(select(EduLevel))
    return result.scalars().all()


async def get_edu_level_by_id(db: AsyncSession, edu_level_id: int):
    result = await db.execute(select(EduLevel).where(EduLevel.id == edu_level_id))
    edu_level = result.scalar_one_or_none()
    if not edu_level:
        raise HTTPException(status_code=404, detail="Уровень образования не найден")
    return edu_level


async def create_edu_level(db: AsyncSession, data: EduLevelCreate):
    edu_level = EduLevel(**data.dict())
    db.add(edu_level)
    await db.commit()
    await db.refresh(edu_level)
    return edu_level


async def update_edu_level(db: AsyncSession, edu_level_id: int, data: EduLevelUpdate):
    edu_level = await get_edu_level_by_id(db, edu_level_id)
    for key, value in data.dict().items():
        setattr(edu_level, key, value)
    await db.commit()
    await db.refresh(edu_level)
    return edu_level


async def delete_edu_level(db: AsyncSession, edu_level_id: int):
    edu_level = await get_edu_level_by_id(db, edu_level_id)
    await db.delete(edu_level)
    await db.commit()
