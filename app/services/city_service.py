from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate
from fastapi import HTTPException

async def get_all_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()

async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

async def create_city(db: AsyncSession, data: CityCreate):
    city = City(**data.dict())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city

async def update_city(db: AsyncSession, city_id: int, data: CityUpdate):
    city = await get_city_by_id(db, city_id)
    for key, value in data.dict().items():
        setattr(city, key, value)
    await db.commit()
    await db.refresh(city)
    return city

async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db, city_id)
    await db.delete(city)
    await db.commit()