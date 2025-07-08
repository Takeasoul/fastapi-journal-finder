from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.city import CityCreate, CityUpdate, CityOut
from app.services import city_service

router = APIRouter()

@router.get("/", response_model=list[CityOut],  dependencies=[Depends(require_role("user"))])
async def list_cities(db: AsyncSession = Depends(get_db1_session)):
    return await city_service.get_all_cities(db)

@router.get("/{city_id}", response_model=CityOut,  dependencies=[Depends(require_role("user"))])
async def get_city(city_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await city_service.get_city_by_id(db, city_id)

@router.post("/", response_model=CityOut,  dependencies=[Depends(require_role("admin"))])
async def create_city(data: CityCreate, db: AsyncSession = Depends(get_db1_session)):
    return await city_service.create_city(db, data)

@router.put("/{city_id}", response_model=CityOut,  dependencies=[Depends(require_role("admin"))])
async def update_city(city_id: int, data: CityUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await city_service.update_city(db, city_id, data)

@router.delete("/{city_id}",  dependencies=[Depends(require_role("admin"))])
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db1_session)):
    await city_service.delete_city(db, city_id)
    return {"detail": "City deleted"}