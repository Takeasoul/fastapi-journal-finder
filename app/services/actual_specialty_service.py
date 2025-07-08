from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.actual_specialty import ActualSpecialty
from app.schemas.actual_specialty import ActualSpecialtyCreate, ActualSpecialtyUpdate

async def get_all_actual_specialties(db: AsyncSession):
    result = await db.execute(select(ActualSpecialty))
    return result.scalars().all()

async def get_actual_specialty_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(ActualSpecialty).where(ActualSpecialty.id == id))
    return result.scalar_one_or_none()

async def create_actual_specialty(db: AsyncSession, data: ActualSpecialtyCreate):
    record = ActualSpecialty(**data.dict())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

async def update_actual_specialty(db: AsyncSession, id: int, data: ActualSpecialtyUpdate):
    record = await get_actual_specialty_by_id(db, id)
    if not record:
        return None
    for field, value in data.dict().items():
        setattr(record, field, value)
    await db.commit()
    await db.refresh(record)
    return record

async def delete_actual_specialty(db: AsyncSession, id: int):
    record = await get_actual_specialty_by_id(db, id)
    if not record:
        return False
    await db.delete(record)
    await db.commit()
    return True
