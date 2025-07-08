from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.main_section import MainSectionCreate, MainSectionUpdate, MainSectionOut
from app.services import main_section_service

router = APIRouter()

@router.get("/", response_model=list[MainSectionOut],  dependencies=[Depends(require_role("user"))])
async def list_main_sections(db: AsyncSession = Depends(get_db1_session)):
    return await main_section_service.get_all_main_sections(db)

@router.get("/{id}", response_model=MainSectionOut,  dependencies=[Depends(require_role("user"))])
async def get_main_section(id: int, db: AsyncSession = Depends(get_db1_session)):
    record = await main_section_service.get_main_section_by_id(db, id)
    if not record:
        raise HTTPException(status_code=404, detail="Main section not found")
    return record

@router.post("/", response_model=MainSectionOut,  dependencies=[Depends(require_role("admin"))])
async def create_main_section(data: MainSectionCreate, db: AsyncSession = Depends(get_db1_session)):
    return await main_section_service.create_main_section(db, data)

@router.put("/{id}", response_model=MainSectionOut,  dependencies=[Depends(require_role("admin"))])
async def update_main_section(id: int, data: MainSectionUpdate, db: AsyncSession = Depends(get_db1_session)):
    record = await main_section_service.update_main_section(db, id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Main section not found")
    return record

@router.delete("/{id}",  dependencies=[Depends(require_role("admin"))])
async def delete_main_section(id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await main_section_service.delete_main_section(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Main section not found")
    return {"detail": "Deleted"}
