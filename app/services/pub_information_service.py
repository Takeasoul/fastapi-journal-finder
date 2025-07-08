from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.models.pub_information import PubInformation
from app.schemas.pub_information import PubInformationCreate, PubInformationUpdate

async def get_pub_info(db: AsyncSession, pub_id: int):
    result = await db.execute(select(PubInformation).where(PubInformation.pub_id == pub_id))
    pub_info = result.scalars().first()
    if not pub_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication info not found")
    return pub_info

async def create_pub_info(db: AsyncSession, pub_info_in: PubInformationCreate):
    pub_info = PubInformation(**pub_info_in.dict())
    db.add(pub_info)
    await db.commit()
    await db.refresh(pub_info)
    return pub_info

async def update_pub_info(db: AsyncSession, pub_id: int, pub_info_in: PubInformationUpdate):
    pub_info = await get_pub_info(db, pub_id)
    for field, value in pub_info_in.dict(exclude_unset=True).items():
        setattr(pub_info, field, value)
    db.add(pub_info)
    await db.commit()
    await db.refresh(pub_info)
    return pub_info

async def delete_pub_info(db: AsyncSession, pub_id: int):
    pub_info = await get_pub_info(db, pub_id)
    await db.delete(pub_info)
    await db.commit()
