from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.edu_level import (
    EduLevelOut,
    EduLevelCreate,
    EduLevelUpdate
)
from app.services import edu_level_service

router = APIRouter()


@router.get("/", response_model=list[EduLevelOut],  dependencies=[Depends(require_role("user"))])
async def list_edu_levels(db: AsyncSession = Depends(get_db1_session)):
    return await edu_level_service.get_all_edu_levels(db)


@router.get("/{edu_level_id}", response_model=EduLevelOut,  dependencies=[Depends(require_role("user"))])
async def get_edu_level(edu_level_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await edu_level_service.get_edu_level_by_id(db, edu_level_id)


@router.post("/", response_model=EduLevelOut,  dependencies=[Depends(require_role("admin"))])
async def create_edu_level(data: EduLevelCreate, db: AsyncSession = Depends(get_db1_session)):
    return await edu_level_service.create_edu_level(db, data)


@router.put("/{edu_level_id}", response_model=EduLevelOut,  dependencies=[Depends(require_role("admin"))])
async def update_edu_level(edu_level_id: int, data: EduLevelUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await edu_level_service.update_edu_level(db, edu_level_id, data)


@router.delete("/{edu_level_id}",  dependencies=[Depends(require_role("admin"))])
async def delete_edu_level(edu_level_id: int, db: AsyncSession = Depends(get_db1_session)):
    await edu_level_service.delete_edu_level(db, edu_level_id)
    return {"detail": "EduLevel deleted"}