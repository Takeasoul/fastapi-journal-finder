from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.actual_grnti import ActualGRNTI
from app.schemas.actual_grnti import ActualGRNTICreate, ActualGRNTIUpdate

async def get_all_actual_grnti(db: AsyncSession):
    result = await db.execute(select(ActualGRNTI))
    return result.scalars().all()

async def get_actual_grnti_by_id(db: AsyncSession, actual_grnti_id: int):
    result = await db.execute(select(ActualGRNTI).where(ActualGRNTI.id == actual_grnti_id))
    return result.scalar_one_or_none()

async def create_actual_grnti(db: AsyncSession, data: ActualGRNTICreate):
    record = ActualGRNTI(**data.dict())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

async def update_actual_grnti(db: AsyncSession, actual_grnti_id: int, data: ActualGRNTIUpdate):
    record = await get_actual_grnti_by_id(db, actual_grnti_id)
    if record is None:
        return None
    for field, value in data.dict().items():
        setattr(record, field, value)
    await db.commit()
    await db.refresh(record)
    return record

async def delete_actual_grnti(db: AsyncSession, actual_grnti_id: int):
    record = await get_actual_grnti_by_id(db, actual_grnti_id)
    if record is None:
        return False
    await db.delete(record)
    await db.commit()
    return True
