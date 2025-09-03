import logging
from typing import Dict, Tuple, List

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func, text, Enum, exists, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from app.core.security import logger
from app.models import PublicationActualSpecialty, ActualSpecialty
from app.models.publication import Publication
from app.models.publication_base_info import PublicationBaseInfo
from app.schemas.actual_grnti import ActualGRNTIBase, ActualGRNTIResponse
from app.schemas.actual_oecd import ActualOECDBase, ActualOECDResponse
from app.schemas.index import IndexResponse
from app.schemas.main_section import MainSectionBase, MainSectionResponse
from app.schemas.pub_information import PubInformationResponse
from app.schemas.publication import PublicationCreate, PublicationUpdate, PublicationOut, PublicationResponse, \
    PublicationFilterWithSpec, PublicationResponseWith
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
from app.schemas.publication_base_info import VakCategoryEnum


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

    query = select(Publication).options(
        selectinload(Publication.actual_oecd_items),
        selectinload(Publication.actual_grnti_items),
        selectinload(Publication.main_sections)
    )

    # Initialize the count query without eager loading
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
    publications = result.unique().scalars().all()

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    publications_out = []
    for pub in publications:
        pub_dict = {
            **pub.__dict__,
            "actual_oecd_items": [ActualOECDResponse.model_validate(item.__dict__) for item in pub.actual_oecd_items],
            "actual_grnti_items": [ActualGRNTIResponse.model_validate(item.__dict__) for item in
                                   pub.actual_grnti_items],
            "main_sections": [MainSectionResponse.model_validate(item.__dict__) for item in pub.main_sections],
        }
        publications_out.append(PublicationResponse.model_validate(pub_dict))

    return publications_out, total

async def get_publication_by_id(db: AsyncSession, pub_id: int):
    result = await db.execute(
        select(Publication)
        .options(
            selectinload(Publication.actual_oecd_items),
            selectinload(Publication.actual_grnti_items),
            selectinload(Publication.main_sections)
        )
        .where(Publication.id == pub_id)
    )
    pub = result.scalar_one_or_none()
    if not pub:
        raise HTTPException(status_code=404, detail="Публикация не найдена")

    # Преобразуем в Pydantic модель
    pub_dict = {
        **pub.__dict__,
        "actual_oecd_items": [ActualOECDResponse.model_validate(item.__dict__) for item in pub.actual_oecd_items],
        "actual_grnti_items": [ActualGRNTIResponse.model_validate(item.__dict__) for item in pub.actual_grnti_items],
        "main_sections": [MainSectionResponse.model_validate(item.__dict__) for item in pub.main_sections],
    }
    return PublicationOut.model_validate(pub_dict)

async def create_publication(db: AsyncSession, data: PublicationCreate):
    pub = Publication(**data.dict())
    db.add(pub)
    await db.commit()
    await db.refresh(pub)

    # Преобразуем в Pydantic-модель
    return PublicationResponse.model_validate(pub.__dict__)


async def get_publication_by_id_raw(db: AsyncSession, pub_id: int):
    result = await db.execute(
        select(Publication)
        .options(
            selectinload(Publication.actual_oecd_items),
            selectinload(Publication.actual_grnti_items),
            selectinload(Publication.main_sections)
        )
        .where(Publication.id == pub_id)
    )
    return result.scalar_one_or_none()


async def update_publication(db: AsyncSession, pub_id: int, data: PublicationUpdate):
    # Получаем объект SQLAlchemy
    pub = await get_publication_by_id_raw(db, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Публикация не найдена")

    # Обновляем поля объекта SQLAlchemy
    for key, value in data.dict(exclude_unset=True).items():
        setattr(pub, key, value)

    # Сохраняем изменения в базе данных
    await db.commit()

    # Обновляем состояние объекта SQLAlchemy
    await db.refresh(pub)

    # Преобразуем объект SQLAlchemy в Pydantic-модель
    try:
        return PublicationResponse.model_validate({
            **pub.__dict__,
            "actual_oecd_items": [ActualOECDResponse.model_validate(item.__dict__) for item in pub.actual_oecd_items],
            "actual_grnti_items": [ActualGRNTIResponse.model_validate(item.__dict__) for item in pub.actual_grnti_items],
            "main_sections": [MainSectionResponse.model_validate(item.__dict__) for item in pub.main_sections],
        })
    except ValidationError as e:
        logger.error(f"Validation error for publication ID {pub_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")


async def delete_publication(db: AsyncSession, pub_id: int):
    pub = await get_publication_by_id_raw(db, pub_id)
    if pub:
        # Преобразуем в Pydantic-модель перед удалением
        deleted_pub = PublicationResponse.model_validate(pub.__dict__)
        await db.delete(pub)
        await db.commit()
        return {"detail": "Публикация удалена", "deleted_item": deleted_pub}

    raise HTTPException(status_code=404, detail="Публикация не найдена")


async def get_paginated_publication_base_info(
    db: AsyncSession,
    page: int,
    per_page: int,
    filters: dict
):
    query = select(PublicationBaseInfo)
    count_query = select(func.count()).select_from(PublicationBaseInfo)

    # Фильтрация по языкам (SET)
    if "languages" in filters and filters["languages"]:
        for lang in filters["languages"]:
            # Используем FIND_IN_SET для работы с SET
            query = query.where(text(f"FIND_IN_SET('{lang.value}', `Языки`)"))
            count_query = count_query.where(text(f"FIND_IN_SET('{lang.value}', `Языки`)"))

    # Фильтрация по остальным полям
    for key, value in filters.items():
        if key == "languages":
            continue  # уже обработали выше

        if hasattr(PublicationBaseInfo, key) and value is not None:
            column = getattr(PublicationBaseInfo, key)

            # Специальная обработка для vak_category
            if key == "vak_category":
                # Преобразуем значение Enum в строку
                query = query.where(column == value.value if isinstance(value, VakCategoryEnum) else value)
                count_query = count_query.where(column == value.value if isinstance(value, VakCategoryEnum) else value)
            elif isinstance(value, str):
                # Для строковых полей используем ilike
                query = query.where(column.ilike(f"%{value}%"))
                count_query = count_query.where(column.ilike(f"%{value}%"))
            else:
                # Для остальных (например, int) — обычное сравнение
                query = query.where(column == value)
                count_query = count_query.where(column == value)

    # Пагинация
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    # Выполнение запросов
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

            # Специальная обработка для Enum
            if isinstance(column.type, Enum) and isinstance(value, str):
                # Преобразуем значение Enum в строку
                query = query.where(column == value)
                count_query = count_query.where(column == value)
            elif isinstance(value, str):
                # Для строковых полей используем ilike
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


logger = logging.getLogger("publications")
logger.setLevel(logging.INFO)

async def get_paginated_publications_with_index_and_information(
    db: AsyncSession,
    page: int,
    per_page: int,
    filters: dict
) -> Tuple[List[PublicationResponseWith], int]:

    enum_fields = {
        "serial_type": SerialTypeEnum11,
        "serial_elem": SerialElemEnum,
        "purpose": PurposeEnum,
        "distribution": DistributionEnum,
        "access": AccessEnum,
        "main_finance": MainFinanceEnum,
        "multidisc": MultidiscEnum,
    }

    query = select(Publication).options(
        selectinload(Publication.actual_oecd_items),
        selectinload(Publication.actual_grnti_items),
        selectinload(Publication.main_sections),
        joinedload(Publication.pub_information),  # уже правильно
        joinedload(Publication.index),  # вместо selectinload
        selectinload(Publication.actual_specialties)
    )

    count_query = select(func.count()).select_from(Publication)

    # --- фильтры ---
    for key, value in filters.items():
        if not value:
            continue

        if key == "languages":
            lang_conditions = [Publication.language.like(f"%{lang.value}%") for lang in value]
            query = query.where(or_(*lang_conditions))
            count_query = count_query.where(or_(*lang_conditions))
        elif key == "name":
            query = query.where(Publication.name.ilike(f"%{value}%"))
            count_query = count_query.where(Publication.name.ilike(f"%{value}%"))
        elif key == "el_updated_at_from":
            query = query.where(Publication.el_updated_at >= value)
            count_query = count_query.where(Publication.el_updated_at >= value)
        elif key == "el_updated_at_to":
            query = query.where(Publication.el_updated_at <= value)
            count_query = count_query.where(Publication.el_updated_at <= value)
        elif key in enum_fields:
            try:
                enum_value = enum_fields[key](value)
                query = query.where(getattr(Publication, key) == enum_value)
                count_query = count_query.where(getattr(Publication, key) == enum_value)
            except ValueError:
                continue
        elif key == "actual_specialty":
            subq = exists().where(
                (ActualSpecialty.pub_id == Publication.id) &
                (ActualSpecialty.specialty_id.in_(value))
            )
            query = query.where(subq)
            count_query = count_query.where(subq)
        elif hasattr(Publication, key):
            query = query.where(getattr(Publication, key) == value)
            count_query = count_query.where(getattr(Publication, key) == value)

    # --- пагинация ---
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    logger.info(f"Executing count query: {count_query}")
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    logger.info(f"Total publications found: {total}")

    logger.info(f"Executing main query: {query}")
    result = await db.execute(query)
    publications = result.unique().scalars().all()
    logger.info(f"Fetched {len(publications)} publications (page {page})")

    publications_out = []
    for pub in publications:
        logger.info(f"Processing publication ID={pub.id}, name={pub.name}")
        pub_information = None
        if pub.pub_information:
            logger.info(f"PubInformation found for publication ID={pub.id}")
            pub_information_data = {
                field: getattr(pub.pub_information, field)
                for field in PubInformationResponse.__fields__.keys()
            }
            pub_information = PubInformationResponse(**pub_information_data)
        else:
            logger.info(f"No PubInformation for publication ID={pub.id}")

        index = None
        if pub.index:
            logger.info(f"Index found for publication ID={pub.id}")
            index_data = {
                field: getattr(pub.index, field)
                for field in IndexResponse.__fields__.keys()
            }
            index = IndexResponse(**index_data)
        else:
            logger.info(f"No Index for publication ID={pub.id}")

        publications_out.append(
            PublicationResponseWith(
                id=pub.id,
                el_id=pub.el_id,
                vak_id=pub.vak_id,
                name=pub.name,
                serial_type=pub.serial_type,
                serial_elem=pub.serial_elem,
                purpose=pub.purpose,
                distribution=pub.distribution,
                access=pub.access,
                main_finance=pub.main_finance,
                multidisc=pub.multidisc,
                language=list(pub.language) if pub.language else [],
                el_updated_at=pub.el_updated_at,
                actual_oecd_items=[ActualOECDResponse.model_validate(item, from_attributes=True) for item in pub.actual_oecd_items],
                actual_grnti_items=[ActualGRNTIResponse.model_validate(item, from_attributes=True) for item in pub.actual_grnti_items],
                main_sections=[MainSectionResponse.model_validate(item, from_attributes=True) for item in pub.main_sections],
                pub_information=pub_information,
                index=index
            )
        )

    return publications_out, total