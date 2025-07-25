from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db1_session
from app.core.security import require_role, logger
from app.schemas.actual_specialty import ActualSpecialtyCreate, ActualSpecialtyUpdate, ActualSpecialtyOut, \
    ActualSpecialtyResponse, PaginatedActualSpecialtyResponse, ActualSpecialtyFilter
from app.schemas.specialty import SpecialtyResponse
from app.services import actual_specialty_service, publication_service
from app.services.actual_specialty_service import get_paginated_actual_specialty

router = APIRouter()

@router.get(
    "/",
    response_model=PaginatedActualSpecialtyResponse,
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех актуальных специальностей",
    description="Этот эндпоинт возвращает список всех записей актуальных специальностей из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_actual_specialty(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    filters: ActualSpecialtyFilter = Depends()
):
    try:
        filter_dict = filters.model_dump(exclude_none=True)
        result = await actual_specialty_service.get_paginated_actual_specialty(db, page, per_page, filter_dict)
        return PaginatedActualSpecialtyResponse(**result)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_actual_specialty: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get(
    "/{id}",
    response_model=ActualSpecialtyOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить запись актуальной специальности по ID",
    description="Этот эндпоинт возвращает запись актуальной специальности по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_actual_specialty(id: int, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_specialty_service.get_actual_specialty_by_id(db, id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена актуальная специальность")
    return record

@router.post(
    "/",
    response_model=ActualSpecialtyResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новую запись актуальной специальности",
    description="Этот эндпоинт создает новую запись актуальной специальности в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_actual_specialty(data: ActualSpecialtyCreate, db: AsyncSession = Depends(get_db1_session)):
    try:
        record = await actual_specialty_service.create_actual_specialty(db, data)
        return record
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put(
    "/{id}",
    response_model=ActualSpecialtyResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить запись актуальной специальности",
    description="Этот эндпоинт обновляет существующую запись актуальной специальности по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_actual_specialty(id: int, data: ActualSpecialtyUpdate, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_specialty_service.update_actual_specialty(db, id, data)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена актуальная специальность")
    return record

@router.delete(
    "/{id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить запись актуальной специальности",
    description="Этот эндпоинт удаляет запись актуальной специальности по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_actual_specialty(id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await actual_specialty_service.delete_actual_specialty(db, id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена актуальная специальность")
    return {"detail": "Актуальная специальность удалена"}
