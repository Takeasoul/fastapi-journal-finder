from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

async def get_all_contacts(db: AsyncSession):
    result = await db.execute(
        select(Contact).options(joinedload(Contact.city))
    )
    return result.scalars().all()

async def get_contact_by_pub_id(db: AsyncSession, pub_id: int):
    result = await db.execute(
        select(Contact)
        .where(Contact.pub_id == pub_id)
        .options(joinedload(Contact.city))
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Контактная информация не найдена")
    return contact

async def create_contact(db: AsyncSession, contact_in: ContactCreate):
    contact = Contact(**contact_in.dict())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contact(db: AsyncSession, pub_id: int, contact_in: ContactUpdate):
    contact = await get_contact_by_pub_id(db, pub_id)
    for field, value in contact_in.dict(exclude_unset=True).items():
        setattr(contact, field, value)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def delete_contact(db: AsyncSession, pub_id: int):
    contact = await get_contact_by_pub_id(db, pub_id)
    await db.delete(contact)
    await db.commit()
