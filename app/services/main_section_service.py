from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.security import logger
from app.models.main_section import MainSection
from app.schemas.main_section import MainSectionCreate, MainSectionUpdate

async def get_all_main_sections(db: AsyncSession):
    try:
        result = await db.execute(
            select(MainSection)
            .options(joinedload(MainSection.section))
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_all_main_sections: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при получении списка основных разделов")

async def get_main_section_by_id(db: AsyncSession, id: int):
    try:
        result = await db.execute(
            select(MainSection)
            .where(MainSection.id == id)
            .options(joinedload(MainSection.section))
        )
        record = result.scalar_one_or_none()
        if not record:
            raise HTTPException(status_code=404, detail="Основной раздел не найден")
        return record
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_main_section_by_id: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при получении основного раздела")

async def create_main_section(db: AsyncSession, data: MainSectionCreate):
    record = MainSection(**data.dict())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

async def update_main_section(db: AsyncSession, id: int, data: MainSectionUpdate):
    record = await get_main_section_by_id(db, id)
    if not record:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)
    await db.commit()
    await db.refresh(record)
    return record

async def delete_main_section(db: AsyncSession, id: int):
    record = await get_main_section_by_id(db, id)
    if not record:
        return False
    await db.delete(record)
    await db.commit()
    return True
