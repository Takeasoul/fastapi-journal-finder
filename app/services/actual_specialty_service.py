from typing import Tuple, List

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload, Query
from math import ceil
from app.core.security import logger
from app.models import Specialty
from app.models.actual_specialty import ActualSpecialty
from app.schemas.actual_specialty import ActualSpecialtyCreate, ActualSpecialtyUpdate, ActualSpecialtyOut, \
    PaginatedActualSpecialtyResponse
from app.schemas.publication import PublicationBase, PaginatedResponse
from app.schemas.section import SectionOut
from app.schemas.specialty import SpecialtyBase, SpecialtyResponse


async def get_paginated_actual_specialty(
    db: AsyncSession,
    page: int,
    per_page: int,
    filters: dict
) -> dict:
    try:
        query = select(ActualSpecialty).options(
            selectinload(ActualSpecialty.specialty).selectinload(Specialty.level)
        )

        count_query = select(func.count()).select_from(ActualSpecialty)

        # Фильтры
        if "specialty_id" in filters:
            query = query.where(ActualSpecialty.specialty_id == filters["specialty_id"])
            count_query = count_query.where(ActualSpecialty.specialty_id == filters["specialty_id"])
        if "source" in filters:
            query = query.where(ActualSpecialty.source == filters["source"])
            count_query = count_query.where(ActualSpecialty.source == filters["source"])
        if "actual" in filters:
            query = query.where(ActualSpecialty.actual == filters["actual"])
            count_query = count_query.where(ActualSpecialty.actual == filters["actual"])

        # Пагинация
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        result = await db.execute(query)
        specialties = result.scalars().all()

        total_result = await db.execute(count_query)
        total = total_result.scalar_one()
        total_pages = ceil(total / per_page) if per_page else 1

        # Преобразуем в Pydantic
        speciality_out = []

        for spec in specialties:
            print(f"level_id: {spec.specialty.level_id}, level: {spec.specialty.level}")
            specialty_obj = SpecialtyResponse.model_validate(spec.specialty) if spec.specialty else None
            spec_dict = {
                "id": spec.id,
                "pub_id": spec.pub_id,
                "specialty_id": spec.specialty_id,
                "source": spec.source,
                "actual": spec.actual,
                "start_date": spec.start_date,
                "end_date": spec.end_date,
                "specialty": specialty_obj
            }
            speciality_out.append(ActualSpecialtyOut.model_validate(spec_dict))

        return {
            "items": speciality_out,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching actual specialties: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        logger.error(f"Unexpected error while fetching actual specialties: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_actual_specialty_by_id(db: AsyncSession, id: int):
    result = await db.execute(
        select(ActualSpecialty)
        .where(ActualSpecialty.id == id)
        .options(joinedload(ActualSpecialty.specialty))
    )
    return result.scalar_one_or_none()

async def create_actual_specialty(db: AsyncSession, data: ActualSpecialtyCreate):
    record = ActualSpecialty(**data.dict())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

async def update_actual_specialty(db: AsyncSession, id: int, data: ActualSpecialtyUpdate):
    record = await get_actual_specialty_by_id(db, id)
    if not record:
        return None

    for field, value in data.dict(exclude_unset=True).items():  # Игнорируем поля со значением None
        setattr(record, field, value)

    await db.commit()
    await db.refresh(record)
    return record

async def delete_actual_specialty(db: AsyncSession, id: int):
    record = await get_actual_specialty_by_id(db, id)
    if not record:
        return False
    await db.delete(record)
    await db.commit()
    return True
