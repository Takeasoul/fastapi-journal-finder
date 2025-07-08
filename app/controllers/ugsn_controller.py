from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.ugsn import UGSNCreate, UGSNUpdate, UGSNOut
from app.services import ugsn_service

router = APIRouter()

@router.get("/", response_model=list[UGSNOut],  dependencies=[Depends(require_role("user"))])
async def list_ugsn(db: AsyncSession = Depends(get_db1_session)):
    return await ugsn_service.get_all_ugsn(db)

@router.get("/{id}", response_model=UGSNOut,  dependencies=[Depends(require_role("user"))])
async def get_ugsn(id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await ugsn_service.get_ugsn_by_id(db, id)

@router.post("/", response_model=UGSNOut,  dependencies=[Depends(require_role("admin"))])
async def create_ugsn(data: UGSNCreate, db: AsyncSession = Depends(get_db1_session)):
    return await ugsn_service.create_ugsn(db, data)

@router.put("/{id}", response_model=UGSNOut,  dependencies=[Depends(require_role("admin"))])
async def update_ugsn(id: int, data: UGSNUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await ugsn_service.update_ugsn(db, id, data)

@router.delete("/{id}",  dependencies=[Depends(require_role("admin"))])
async def delete_ugsn(id: int, db: AsyncSession = Depends(get_db1_session)):
    await ugsn_service.delete_ugsn(db, id)
    return {"detail": "UGSN deleted"}