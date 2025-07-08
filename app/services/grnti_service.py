from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.grnti import Grnti
from app.schemas.grnti import GrntiCreate, GrntiUpdate

async def get_all_grnti(db: AsyncSession):
    result = await db.execute(select(Grnti))
    return result.scalars().all()

async def get_grnti_by_id(db: AsyncSession, grnti_id: int):
    result = await db.execute(select(Grnti).where(Grnti.id == grnti_id))
    return result.scalar_one_or_none()

async def create_grnti(db: AsyncSession, data: GrntiCreate):
    grnti = Grnti(**data.dict())
    db.add(grnti)
    await db.commit()
    await db.refresh(grnti)
    return grnti

async def update_grnti(db: AsyncSession, grnti_id: int, data: GrntiUpdate):
    grnti = await get_grnti_by_id(db, grnti_id)
    if grnti:
        for key, value in data.dict().items():
            setattr(grnti, key, value)
        await db.commit()
        await db.refresh(grnti)
    return grnti

async def delete_grnti(db: AsyncSession, grnti_id: int):
    grnti = await get_grnti_by_id(db, grnti_id)
    if grnti:
        await db.delete(grnti)
        await db.commit()
