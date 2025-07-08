from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.ugsn import UGSN
from app.schemas.ugsn import UGSNCreate, UGSNUpdate

async def get_all_ugsn(db: AsyncSession):
    result = await db.execute(select(UGSN))
    return result.scalars().all()

async def get_ugsn_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(UGSN).where(UGSN.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="UGSN not found")
    return item

async def create_ugsn(db: AsyncSession, data: UGSNCreate):
    item = UGSN(**data.dict())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def update_ugsn(db: AsyncSession, id: int, data: UGSNUpdate):
    item = await get_ugsn_by_id(db, id)
    for key, value in data.dict().items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return item

async def delete_ugsn(db: AsyncSession, id: int):
    item = await get_ugsn_by_id(db, id)
    await db.delete(item)
    await db.commit()