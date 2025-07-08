from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.index import Index
from app.schemas.index import IndexCreate, IndexUpdate

async def get_all_indexes(db: AsyncSession):
    result = await db.execute(select(Index))
    return result.scalars().all()

async def get_index_by_pub_id(db: AsyncSession, pub_id: int):
    result = await db.execute(select(Index).where(Index.pub_id == pub_id))
    return result.scalar_one_or_none()

async def create_index(db: AsyncSession, data: IndexCreate):
    idx = Index(**data.dict())
    db.add(idx)
    await db.commit()
    await db.refresh(idx)
    return idx

async def update_index(db: AsyncSession, pub_id: int, data: IndexUpdate):
    idx = await get_index_by_pub_id(db, pub_id)
    if idx:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(idx, key, value)
        await db.commit()
        await db.refresh(idx)
    return idx

async def delete_index(db: AsyncSession, pub_id: int):
    idx = await get_index_by_pub_id(db, pub_id)
    if idx:
        await db.delete(idx)
        await db.commit()
