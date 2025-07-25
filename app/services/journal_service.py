from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from app.models.journal import Journal
from app.schemas.journal import JournalCreate, JournalUpdate


async def get_journal_by_id(db: AsyncSession, journal_id: int):
    try:
        result = await db.execute(
            select(Journal)
            .where(Journal.id == journal_id)
            .options(joinedload(Journal.publication))
        )
        journal = result.scalar_one_or_none()
        if not journal:
            raise HTTPException(status_code=404, detail="Журнал не найден")
        return journal
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при получении журнала")

async def get_all_journals(db: AsyncSession):
    try:
        result = await db.execute(select(Journal).options(joinedload(Journal.publication)))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при получении списка журналов")

async def create_journal(db: AsyncSession, data: JournalCreate):
    journal = Journal(**data.dict())
    db.add(journal)
    await db.commit()
    await db.refresh(journal)
    return journal

async def update_journal(db: AsyncSession, journal_id: int, data: JournalUpdate):
    journal = await get_journal_by_id(db, journal_id)
    if journal:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(journal, key, value)
        await db.commit()
        await db.refresh(journal)
    return journal

async def delete_journal(db: AsyncSession, journal_id: int):
    journal = await get_journal_by_id(db, journal_id)
    if journal:
        await db.delete(journal)
        await db.commit()

async def get_paginated_journals(
    db: AsyncSession,
    page: int,
    per_page: int,
    filters: dict
):
    from app.models.journal import Journal

    query = select(Journal).options(selectinload(Journal.publication))
    count_query = select(func.count()).select_from(Journal)

    # Диапазон по дате
    if "last_send_date_from" in filters and filters["last_send_date_from"] is not None:
        query = query.where(Journal.last_send_date >= filters["last_send_date_from"])
        count_query = count_query.where(Journal.last_send_date >= filters["last_send_date_from"])
    if "last_send_date_to" in filters and filters["last_send_date_to"] is not None:
        query = query.where(Journal.last_send_date <= filters["last_send_date_to"])
        count_query = count_query.where(Journal.last_send_date <= filters["last_send_date_to"])

    # Диапазон по price
    if "price_from" in filters and filters["price_from"] is not None:
        query = query.where(Journal.price >= filters["price_from"])
        count_query = count_query.where(Journal.price >= filters["price_from"])
    if "price_to" in filters and filters["price_to"] is not None:
        query = query.where(Journal.price <= filters["price_to"])
        count_query = count_query.where(Journal.price <= filters["price_to"])

    # Диапазон по copyright_fee
    if "copyright_fee_from" in filters and filters["copyright_fee_from"] is not None:
        query = query.where(Journal.copyright_fee >= filters["copyright_fee_from"])
        count_query = count_query.where(Journal.copyright_fee >= filters["copyright_fee_from"])
    if "copyright_fee_to" in filters and filters["copyright_fee_to"] is not None:
        query = query.where(Journal.copyright_fee <= filters["copyright_fee_to"])
        count_query = count_query.where(Journal.copyright_fee <= filters["copyright_fee_to"])

    # Остальные фильтры
    for key, value in filters.items():
        if key in (
            "last_send_date_from", "last_send_date_to",
            "price_from", "price_to",
            "copyright_fee_from", "copyright_fee_to"
        ):
            continue  # уже обработали выше
        if hasattr(Journal, key) and value is not None:
            column = getattr(Journal, key)
            if isinstance(value, str):
                query = query.where(column.ilike(f"%{value}%"))
                count_query = count_query.where(column.ilike(f"%{value}%"))
            else:
                query = query.where(column == value)
                count_query = count_query.where(column == value)

    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    items = result.scalars().all()

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    return items, total