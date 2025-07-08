from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.main_section import MainSection
from app.schemas.main_section import MainSectionCreate, MainSectionUpdate

async def get_all_main_sections(db: AsyncSession):
    result = await db.execute(select(MainSection))
    return result.scalars().all()

async def get_main_section_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(MainSection).where(MainSection.id == id))
    return result.scalar_one_or_none()

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
    for field, value in data.dict().items():
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
