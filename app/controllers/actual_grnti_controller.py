from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.actual_grnti import ActualGRNTICreate, ActualGRNTIUpdate, ActualGRNTIOut
from app.services import actual_grnti_service

router = APIRouter()

@router.get("/", response_model=list[ActualGRNTIOut],  dependencies=[Depends(require_role("user"))])
async def list_actual_grnti(db: AsyncSession = Depends(get_db1_session)):
    return await actual_grnti_service.get_all_actual_grnti(db)

@router.get("/{actual_grnti_id}", response_model=ActualGRNTIOut,  dependencies=[Depends(require_role("user"))])
async def get_actual_grnti(actual_grnti_id: int, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_grnti_service.get_actual_grnti_by_id(db, actual_grnti_id)
    if not record:
        raise HTTPException(status_code=404, detail="Actual GRNTI not found")
    return record

@router.post("/", response_model=ActualGRNTIOut,  dependencies=[Depends(require_role("admin"))])
async def create_actual_grnti(data: ActualGRNTICreate, db: AsyncSession = Depends(get_db1_session)):
    return await actual_grnti_service.create_actual_grnti(db, data)

@router.put("/{actual_grnti_id}", response_model=ActualGRNTIOut,  dependencies=[Depends(require_role("admin"))])
async def update_actual_grnti(actual_grnti_id: int, data: ActualGRNTIUpdate, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_grnti_service.update_actual_grnti(db, actual_grnti_id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Actual GRNTI not found")
    return record

@router.delete("/{actual_grnti_id}",  dependencies=[Depends(require_role("admin"))])
async def delete_actual_grnti(actual_grnti_id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await actual_grnti_service.delete_actual_grnti(db, actual_grnti_id)
    if not success:
        raise HTTPException(status_code=404, detail="Actual GRNTI not found")
    return {"detail": "Actual GRNTI deleted"}
