from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate

async def get_all_sections(db: AsyncSession):
    result = await db.execute(select(Section))
    return result.scalars().all()

async def get_section_by_id(db: AsyncSession, section_id: int):
    result = await db.execute(select(Section).where(Section.id == section_id))
    return result.scalar_one_or_none()

async def create_section(db: AsyncSession, data: SectionCreate):
    new_section = Section(**data.dict())
    db.add(new_section)
    await db.commit()
    await db.refresh(new_section)
    return new_section

async def update_section(db: AsyncSession, section_id: int, data: SectionUpdate):
    section = await get_section_by_id(db, section_id)
    if section:
        for key, value in data.dict().items():
            setattr(section, key, value)
        await db.commit()
        await db.refresh(section)
    return section

async def delete_section(db: AsyncSession, section_id: int):
    section = await get_section_by_id(db, section_id)
    if section:
        await db.delete(section)
        await db.commit()