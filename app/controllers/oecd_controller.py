from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.future import select

from app.core.security import require_role
from app.schemas.pub_information import PubInformationOut, PubInformationCreate, PubInformationUpdate
from app.core.database import get_db1_session
from app.models.pub_information import PubInformation
from app.services.pub_information_service import get_pub_info, create_pub_info, update_pub_info, delete_pub_info

router = APIRouter()

@router.get("/", response_model=List[PubInformationOut],  dependencies=[Depends(require_role("user"))])
async def read_pub_informations(db: AsyncSession = Depends(get_db1_session)):
    result = await db.execute(select(PubInformation))
    return result.scalars().all()

@router.get("/{pub_id}", response_model=PubInformationOut,  dependencies=[Depends(require_role("user"))])
async def read_pub_information(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await get_pub_info(db, pub_id)

@router.post("/", response_model=PubInformationOut, status_code=status.HTTP_201_CREATED,  dependencies=[Depends(require_role("admin"))])
async def create_pub_information(pub_info: PubInformationCreate, db: AsyncSession = Depends(get_db1_session)):
    return await create_pub_info(db, pub_info)

@router.put("/{pub_id}", response_model=PubInformationOut,  dependencies=[Depends(require_role("admin"))])
async def update_pub_information(pub_id: int, pub_info: PubInformationUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await update_pub_info(db, pub_id, pub_info)

@router.delete("/{pub_id}", status_code=status.HTTP_204_NO_CONTENT,  dependencies=[Depends(require_role("admin"))])
async def delete_pub_information(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    await delete_pub_info(db, pub_id)