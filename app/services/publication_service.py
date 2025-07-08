from typing import Dict, Tuple, List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import PublicationActualSpecialty
from app.models.publication import Publication
from app.models.publication_base_info import PublicationBaseInfo
from app.schemas.publication import PublicationCreate, PublicationUpdate
from app.models.publication import (
    Publication,
    SerialTypeEnum11,
    SerialElemEnum,
    PurposeEnum,
    DistributionEnum,
    AccessEnum,
    MainFinanceEnum,
    MultidiscEnum,
)

async def get_paginated_publications(
    db: AsyncSession,
    page: int,
    per_page: int,
    filters: dict
) -> Tuple[List[Publication], int]:
    enum_fields = {
        "serial_type": SerialTypeEnum11,
        "serial_elem": SerialElemEnum,
        "purpose": PurposeEnum,
        "distribution": DistributionEnum,
        "access": AccessEnum,
        "main_finance": MainFinanceEnum,
        "multidisc": MultidiscEnum,
    }

    query = select(Publication)
    count_query = select(func.count()).select_from(Publication)

    # Фильтрация по языкам (Enum)
    if "languages" in filters and filters["languages"]:
        for lang in filters["languages"]:
            query = query.where(Publication.language.like(f"%{lang.value}%"))
            count_query = count_query.where(Publication.language.like(f"%{lang.value}%"))

    # Фильтрация по остальным полям
    for key, value in filters.items():
        if key == "languages":
            continue  # уже обработали выше
        if key == "name" and value:
            query = query.where(Publication.name.ilike(f"%{value}%"))
            count_query = count_query.where(Publication.name.ilike(f"%{value}%"))
        elif key == "el_updated_at_from" and value:
            query = query.where(Publication.el_updated_at >= value)
            count_query = count_query.where(Publication.el_updated_at >= value)
        elif key == "el_updated_at_to" and value:
            query = query.where(Publication.el_updated_at <= value)
            count_query = count_query.where(Publication.el_updated_at <= value)
        elif hasattr(Publication, key):
            if key in enum_fields and value is not None:
                try:
                    enum_value = enum_fields[key](value)
                except ValueError:
                    continue
                query = query.where(getattr(Publication, key) == enum_value)
                count_query = count_query.where(getattr(Publication, key) == enum_value)
            elif value is not None:
                query = query.where(getattr(Publication, key) == value)
                count_query = count_query.where(getattr(Publication, key) == value)

    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    publications = result.scalars().all()

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    return publications, total

async def get_all_publications(db: AsyncSession):
    result = await db.execute(select(Publication))
    return result.scalars().all()

async def get_publication_by_id(db: AsyncSession, pub_id: int):
    result = await db.execute(select(Publication).where(Publication.id == pub_id))
    return result.scalar_one_or_none()

async def create_publication(db: AsyncSession, data: PublicationCreate):
    pub = Publication(**data.dict())
    db.add(pub)
    await db.commit()
    await db.refresh(pub)
    return pub

async def update_publication(db: AsyncSession, pub_id: int, data: PublicationUpdate):
    pub = await get_publication_by_id(db, pub_id)
    if pub:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(pub, key, value)
        await db.commit()
        await db.refresh(pub)
    return pub

async def delete_publication(db: AsyncSession, pub_id: int):
    pub = await get_publication_by_id(db, pub_id)
    if pub:
        await db.delete(pub)
        await db.commit()


async def get_paginated_publication_base_info(
    db: AsyncSession,
    page: int,
    per_page: int,
    filters: dict
):
    query = select(PublicationBaseInfo)
    count_query = select(func.count()).select_from(PublicationBaseInfo)

    # Фильтрация по языкам (Enum)
    if "languages" in filters and filters["languages"]:
        for lang in filters["languages"]:
            query = query.where(PublicationBaseInfo.languages.like(f"%{lang.value}%"))
            count_query = count_query.where(PublicationBaseInfo.languages.like(f"%{lang.value}%"))

    # Фильтрация по остальным полям через LIKE
    for key, value in filters.items():
        if key == "languages":
            continue  # уже обработали выше
        if hasattr(PublicationBaseInfo, key) and value is not None:
            column = getattr(PublicationBaseInfo, key)
            # Для строковых полей используем ilike
            if isinstance(value, str):
                query = query.where(column.ilike(f"%{value}%"))
                count_query = count_query.where(column.ilike(f"%{value}%"))
            else:
                # Для остальных (например, int) — обычное сравнение
                query = query.where(column == value)
                count_query = count_query.where(column == value)

    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    items = result.scalars().all()

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    return items, total


async def get_paginated_publication_actual_specialty(
    db: AsyncSession,
    page: int,
    per_page: int,
    filters: dict
):
    query = select(PublicationActualSpecialty)
    count_query = select(func.count()).select_from(PublicationActualSpecialty)

    for key, value in filters.items():
        if hasattr(PublicationActualSpecialty, key) and value is not None:
            column = getattr(PublicationActualSpecialty, key)
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