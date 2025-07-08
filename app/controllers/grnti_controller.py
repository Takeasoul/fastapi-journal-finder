from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.grnti import GrntiCreate, GrntiUpdate, GrntiOut
from app.services import grnti_service

router = APIRouter()

@router.get("/", response_model=list[GrntiOut],  dependencies=[Depends(require_role("user"))])
async def list_grnti(db: AsyncSession = Depends(get_db1_session)):
    return await grnti_service.get_all_grnti(db)

@router.get("/{grnti_id}", response_model=GrntiOut,  dependencies=[Depends(require_role("user"))])
async def get_grnti(grnti_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await grnti_service.get_grnti_by_id(db, grnti_id)

@router.post("/", response_model=GrntiOut,  dependencies=[Depends(require_role("admin"))])
async def create_grnti(data: GrntiCreate, db: AsyncSession = Depends(get_db1_session)):
    return await grnti_service.create_grnti(db, data)

@router.put("/{grnti_id}", response_model=GrntiOut,  dependencies=[Depends(require_role("admin"))])
async def update_grnti(grnti_id: int, data: GrntiUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await grnti_service.update_grnti(db, grnti_id, data)

@router.delete("/{grnti_id}",  dependencies=[Depends(require_role("admin"))])
async def delete_grnti(grnti_id: int, db: AsyncSession = Depends(get_db1_session)):
    await grnti_service.delete_grnti(db, grnti_id)
    return {"detail": "Grnti deleted"}
