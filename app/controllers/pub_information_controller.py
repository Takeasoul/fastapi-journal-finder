from fastapi import APIRouter, Depends, Path, status
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_role
from app.models.pub_information import PubInformation
from app.schemas.pub_information import PubInformationOut, PubInformationCreate, PubInformationUpdate
from app.core.database import get_db1_session
from app.services.pub_information_service import (
    get_pub_info, create_pub_info, update_pub_info, delete_pub_info
)

router = APIRouter()

@router.get("/", response_model=List[PubInformationOut],  dependencies=[Depends(require_role("user"))])
async def list_pub_infos(db: AsyncSession = Depends(get_db1_session)):
    # Опционально реализовать: получить все записи (если нужно)
    # Или убрать если не нужно
    result = await db.execute(select(PubInformation))
    return result.scalars().all()

@router.get("/{pub_id}", response_model=PubInformationOut,  dependencies=[Depends(require_role("user"))])
async def get_pub_information(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await get_pub_info(db, pub_id)

@router.post("/", response_model=PubInformationOut, status_code=status.HTTP_201_CREATED,  dependencies=[Depends(require_role("admin"))])
async def create_pub_information(data: PubInformationCreate, db: AsyncSession = Depends(get_db1_session)):
    return await create_pub_info(db, data)

@router.put("/{pub_id}", response_model=PubInformationOut,  dependencies=[Depends(require_role("admin"))])
async def update_pub_information(pub_id: int, data: PubInformationUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await update_pub_info(db, pub_id, data)

@router.delete("/{pub_id}", status_code=status.HTTP_204_NO_CONTENT,  dependencies=[Depends(require_role("admin"))])
async def delete_pub_information(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    await delete_pub_info(db, pub_id)
