from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from app.models.specialty import Specialty
from app.schemas.specialty import SpecialtyCreate, SpecialtyUpdate

async def get_all_specialties(db: AsyncSession):
    result = await db.execute(
        select(Specialty).options(selectinload(Specialty.level))
    )
    return result.scalars().all()

async def get_specialty_by_id(db: AsyncSession, specialty_id: int):
    result = await db.execute(
        select(Specialty)
        .options(selectinload(Specialty.level))
        .where(Specialty.id == specialty_id)
    )
    specialty = result.scalar_one_or_none()
    if not specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    return specialty

async def create_specialty(db: AsyncSession, data: SpecialtyCreate):
    new_specialty = Specialty(**data.dict())
    db.add(new_specialty)
    await db.commit()
    await db.refresh(new_specialty)
    return new_specialty

async def update_specialty(db: AsyncSession, specialty_id: int, data: SpecialtyUpdate):
    specialty = await get_specialty_by_id(db, specialty_id)
    for field, value in data.dict().items():
        setattr(specialty, field, value)
    await db.commit()
    await db.refresh(specialty)
    return specialty

async def delete_specialty(db: AsyncSession, specialty_id: int):
    specialty = await get_specialty_by_id(db, specialty_id)
    await db.delete(specialty)
    await db.commit()