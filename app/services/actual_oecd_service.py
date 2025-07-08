from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.actual_oecd import ActualOECD
from app.schemas.actual_oecd import ActualOECDCreate, ActualOECDUpdate

async def get_all_actual_oecd(db: AsyncSession):
    result = await db.execute(select(ActualOECD))
    return result.scalars().all()

async def get_actual_oecd_by_id(db: AsyncSession, actual_oecd_id: int):
    result = await db.execute(select(ActualOECD).where(ActualOECD.id == actual_oecd_id))
    return result.scalar_one_or_none()

async def create_actual_oecd(db: AsyncSession, data: ActualOECDCreate):
    record = ActualOECD(**data.dict())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

async def update_actual_oecd(db: AsyncSession, actual_oecd_id: int, data: ActualOECDUpdate):
    record = await get_actual_oecd_by_id(db, actual_oecd_id)
    if not record:
        return None
    for field, value in data.dict().items():
        setattr(record, field, value)
    await db.commit()
    await db.refresh(record)
    return record

async def delete_actual_oecd(db: AsyncSession, actual_oecd_id: int):
    record = await get_actual_oecd_by_id(db, actual_oecd_id)
    if not record:
        return False
    await db.delete(record)
    await db.commit()
    return True
