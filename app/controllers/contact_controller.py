from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut
from app.services import contact_service

router = APIRouter()

@router.get("/", response_model=list[ContactOut],  dependencies=[Depends(require_role("user"))])
async def list_contacts(db: AsyncSession = Depends(get_db1_session)):
    return await contact_service.get_all_contacts(db)

@router.get("/{pub_id}", response_model=ContactOut,  dependencies=[Depends(require_role("user"))])
async def get_contact(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await contact_service.get_contact_by_pub_id(db, pub_id)

@router.post("/", response_model=ContactOut,  dependencies=[Depends(require_role("admin"))])
async def create_contact(data: ContactCreate, db: AsyncSession = Depends(get_db1_session)):
    return await contact_service.create_contact(db, data)

@router.put("/{pub_id}", response_model=ContactOut,  dependencies=[Depends(require_role("admin"))])
async def update_contact(pub_id: int, data: ContactUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await contact_service.update_contact(db, pub_id, data)

@router.delete("/{pub_id}",  dependencies=[Depends(require_role("admin"))])
async def delete_contact(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    await contact_service.delete_contact(db, pub_id)
    return {"detail": "Contact deleted"}
