from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from app.core.logger import logger
from app.models.specialty import Specialty
from app.schemas.edu_level import EduLevelBase, EduLevelOut
from app.schemas.specialty import SpecialtyCreate, SpecialtyUpdate, SpecialtyOut, SpecialtyResponse
from app.schemas.ugsn import UGSNBase, UGSNOut


async def get_all_specialties(db: AsyncSession):
    try:
        # Выполняем запрос с загрузкой связанных объектов
        result = await db.execute(
            select(Specialty).options(
                selectinload(Specialty.level),
                selectinload(Specialty.ugsn_rel)
            )
        )
        specialties = result.scalars().all()

        # Преобразуем каждую специальность в Pydantic-модель через словарь
        return [
            SpecialtyOut(
                **{
                    "id": specialty.id,
                    "code": specialty.code,
                    "name": specialty.name,
                    "ugsn": UGSNOut.model_validate(specialty.ugsn_rel) if specialty.ugsn_rel else None,
                    "level": EduLevelOut.model_validate(specialty.level) if specialty.level else None
                }
            )
            for specialty in specialties
        ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_specialty_by_id(db: AsyncSession, specialty_id: int):
    try:
        result = await db.execute(
            select(Specialty)
            .options(
                selectinload(Specialty.level),
                selectinload(Specialty.ugsn_rel)
            )
            .where(Specialty.id == specialty_id)
        )
        specialty = result.scalar_one_or_none()
        if not specialty:
            raise HTTPException(status_code=404, detail="Специальность не найдена")

        # Преобразуем в Pydantic-модель
        try:
            return SpecialtyOut.model_validate({
                **specialty.__dict__,
                "level": EduLevelOut.model_validate(specialty.level.__dict__) if specialty.level else None,
                "ugsn": UGSNOut.model_validate(specialty.ugsn_rel.__dict__) if specialty.ugsn_rel else None,
            })
        except ValidationError as e:
            logger.error(f"Validation error for specialty ID {specialty_id}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except SQLAlchemyError as e:
        logger.error(f"Database error for specialty ID {specialty_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_specialty(db: AsyncSession, data: SpecialtyCreate):
    try:
        # Создаем новую специальность
        new_specialty = Specialty(**data.dict())
        db.add(new_specialty)
        await db.commit()

        # Загружаем связанные объекты (например, 'level') с помощью refresh
        await db.refresh(new_specialty, attribute_names=["level", "ugsn_rel"])

        # Преобразуем объект SQLAlchemy в Pydantic-модель
        return SpecialtyResponse(
            id=new_specialty.id,
            code=new_specialty.code,
            name=new_specialty.name,
            ugsn=new_specialty.ugsn,
            level=new_specialty.level_id
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_specialty_by_id_raw(db: AsyncSession, specialty_id: int):
    result = await db.execute(
        select(Specialty)
        .options(
            selectinload(Specialty.level),
            selectinload(Specialty.ugsn_rel)
        )
        .where(Specialty.id == specialty_id)
    )
    return result.scalar_one_or_none()

async def update_specialty(db: AsyncSession, specialty_id: int, data: SpecialtyUpdate):
    try:
        # Получаем "сырой" объект SQLAlchemy
        specialty = await get_specialty_by_id_raw(db, specialty_id)

        # Обновляем поля объекта
        for field, value in data.dict(exclude_unset=True).items():
            setattr(specialty, field, value)

        # Сохраняем изменения
        await db.commit()

        # Обновляем состояние объекта
        await db.refresh(specialty)

        # Преобразуем в Pydantic-модель
        return SpecialtyResponse.model_validate({
            "id": specialty.id,
            "code": specialty.code,
            "name": specialty.name,
            "ugsn": specialty.ugsn,
            "level": specialty.level_id,
        })
    except SQLAlchemyError as e:
        logger.error(f"Database error for specialty ID {specialty_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_specialty(db: AsyncSession, specialty_id: int):
    try:
        specialty = await get_specialty_by_id_raw(db, specialty_id)
        await db.delete(specialty)
        await db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Datab ase error: {str(e)}")