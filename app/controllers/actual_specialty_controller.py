from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.actual_specialty import ActualSpecialtyCreate, ActualSpecialtyUpdate, ActualSpecialtyOut
from app.services import actual_specialty_service

router = APIRouter()

@router.get("/", response_model=list[ActualSpecialtyOut],  dependencies=[Depends(require_role("user"))])
async def list_actual_specialties(db: AsyncSession = Depends(get_db1_session)):
    return await actual_specialty_service.get_all_actual_specialties(db)

@router.get("/{id}", response_model=ActualSpecialtyOut,  dependencies=[Depends(require_role("user"))])
async def get_actual_specialty(id: int, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_specialty_service.get_actual_specialty_by_id(db, id)
    if not record:
        raise HTTPException(status_code=404, detail="Actual specialty not found")
    return record

@router.post("/", response_model=ActualSpecialtyOut,  dependencies=[Depends(require_role("admin"))])
async def create_actual_specialty(data: ActualSpecialtyCreate, db: AsyncSession = Depends(get_db1_session)):
    return await actual_specialty_service.create_actual_specialty(db, data)

@router.put("/{id}", response_model=ActualSpecialtyOut,  dependencies=[Depends(require_role("admin"))])
async def update_actual_specialty(id: int, data: ActualSpecialtyUpdate, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_specialty_service.update_actual_specialty(db, id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Actual specialty not found")
    return record

@router.delete("/{id}",  dependencies=[Depends(require_role("admin"))])
async def delete_actual_specialty(id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await actual_specialty_service.delete_actual_specialty(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Actual specialty not found")
    return {"detail": "Deleted"}
