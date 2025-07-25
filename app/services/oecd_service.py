from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.oecd import OECD
from app.schemas.oecd import OECDCreate, OECDUpdate

async def get_all_oecd(db: AsyncSession):
    result = await db.execute(select(OECD))
    return result.scalars().all()

async def get_oecd_by_id(db: AsyncSession, oecd_id: int):
    result = await db.execute(select(OECD).where(OECD.id == oecd_id))
    return result.scalar_one_or_none()

async def create_oecd(db: AsyncSession, data: OECDCreate):
    oecd = OECD(**data.dict())
    db.add(oecd)
    await db.commit()
    await db.refresh(oecd)
    return oecd

async def update_oecd(db: AsyncSession, oecd_id: int, data: OECDUpdate):
    oecd = await get_oecd_by_id(db, oecd_id)
    if oecd is None:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(oecd, field, value)
    await db.commit()
    await db.refresh(oecd)
    return oecd

async def delete_oecd(db: AsyncSession, oecd_id: int):
    oecd = await get_oecd_by_id(db, oecd_id)
    if oecd is None:
        return False
    await db.delete(oecd)
    await db.commit()
    return True
