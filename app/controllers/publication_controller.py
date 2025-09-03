import json
from datetime import date
from math import ceil
from typing import Optional, List

from fastapi import APIRouter, Depends, Path, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role, logger
from app.schemas.publication import PublicationOut, PublicationCreate, PublicationUpdate, PaginatedResponse, \
    PublicationFilter, PublicationResponse, PublicationFilterWithSpec, PaginatedResponseWith, SerialTypeEnum11, \
    SerialElemEnum, PurposeEnum, DistributionEnum, AccessEnum, MainFinanceEnum, MultidiscEnum, LanguageEnum
from app.schemas.publication_actual_specialty import PublicationActualSpecialtyOut, PublicationActualSpecialtyFilter, \
    PublicationActualSpecialtyResponse
from app.schemas.publication_base_info import PublicationBaseInfoOut, PaginatedBaseInfoResponse, \
    PublicationBaseInfoFilter
from app.services import publication_service

router = APIRouter()

@router.get(
    "/",
    response_model=PaginatedResponse,
    dependencies=[Depends(require_role("user"))],
    description="Получает список всех публикаций с поддержкой пагинации и фильтрации. - **page**: Номер страницы (начинается с 1). - **per_page**: Количество элементов на странице (максимум 100). - **filters**: Фильтры для поиска публикаций (например, язык, автор, дата). ВАЖНО: из-за бага Swagger параметр languages нужно передавать через query (?languages=русский&languages=английский), а не через body, даже если Swagger предлагает body."
)
async def list_publications_paginated(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    filters: PublicationFilter = Depends()
):
    try:
        filter_dict = filters.model_dump(exclude_none=True)
        publications, total = await publication_service.get_paginated_publications(db, page, per_page, filter_dict)
        total_pages = ceil(total / per_page)
        return PaginatedResponse(
            items=publications,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_publications_paginated: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get(
    "/with_index_and_information",
    response_model=PaginatedResponseWith,
    dependencies=[Depends(require_role("user"))],
    description="Получает список всех публикаций с поддержкой пагинации и фильтрации. - **page**: Номер страницы (начинается с 1). - **per_page**: Количество элементов на странице (максимум 100). - **filters**: Фильтры для поиска публикаций (например, язык, автор, дата). ВАЖНО: из-за бага Swagger параметр languages нужно передавать через query (?languages=русский&languages=английский), а не через body, даже если Swagger предлагает body."
)
async def list_publications_paginated(
        db: AsyncSession = Depends(get_db1_session),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100),
        speciality_id: Optional[List[int]] = Query(None),  # Явно обрабатываем speciality_id
        el_id: Optional[int] = Query(None),
        vak_id: Optional[int] = Query(None),
        name: Optional[str] = Query(None),
        serial_type: Optional[SerialTypeEnum11] = Query(None),
        serial_elem: Optional[SerialElemEnum] = Query(None),
        purpose: Optional[PurposeEnum] = Query(None),
        distribution: Optional[DistributionEnum] = Query(None),
        access: Optional[AccessEnum] = Query(None),
        main_finance: Optional[MainFinanceEnum] = Query(None),
        multidisc: Optional[MultidiscEnum] = Query(None),
        languages: Optional[List[LanguageEnum]] = Query(None),  # Изменено на List вместо Set
        el_updated_at_from: Optional[date] = Query(None),
        el_updated_at_to: Optional[date] = Query(None),
):
    try:
        # Формируем словарь фильтров вручную
        filter_dict = {
            "el_id": el_id,
            "vak_id": vak_id,
            "name": name,
            "serial_type": serial_type,
            "serial_elem": serial_elem,
            "purpose": purpose,
            "distribution": distribution,
            "access": access,
            "main_finance": main_finance,
            "multidisc": multidisc,
            "languages": languages,
            "el_updated_at_from": el_updated_at_from,
            "el_updated_at_to": el_updated_at_to,
            "speciality_id": speciality_id,
        }
        # Удаляем ключи с None значениями
        filter_dict = {k: v for k, v in filter_dict.items() if v is not None}

        logger.info(f"Received query parameters: {filter_dict}")

        publications, total = await publication_service.get_paginated_publications_with_index_and_information(
            db, page, per_page, filter_dict
        )
        total_pages = ceil(total / per_page)
        return PaginatedResponseWith(
            items=publications,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_publications_paginated: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get(
    "/getallwithbaseinfo",
    response_model=PaginatedBaseInfoResponse,
    dependencies=[Depends(require_role("user"))],
    description=" Получает список базовой информации о публикациях с поддержкой пагинации и фильтрации. - **page**: Номер страницы (начинается с 1). - **per_page**: Количество элементов на странице (максимум 100). - **filters**: Фильтры для поиска базовой информации (например, язык, автор, дата).ВАЖНО: из-за бага Swagger параметр languages нужно передавать через query (?languages=русский&languages=английский), а не через body, даже если Swagger предлагает body."
)
async def list_publication_base_info(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    filters: PublicationBaseInfoFilter = Depends()
):
    filter_dict = filters.model_dump(exclude_none=True)
    items, total = await publication_service.get_paginated_publication_base_info(db, page, per_page, filter_dict)
    total_pages = ceil(total / per_page)
    return PaginatedBaseInfoResponse(
        items=[PublicationBaseInfoOut.model_validate(obj) for obj in items],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/getallwithactualspecialty", response_model=PublicationActualSpecialtyResponse,  dependencies=[Depends(require_role("user"))], description = " Получает список публикаций с актуальными специальностями с поддержкой пагинации и фильтрации. **page**: Номер страницы (начинается с 1). - **per_page**: Количество элементов на странице (максимум 100). - **filters**: Фильтры для поиска публикаций (например, специальность, дата).")
async def list_publication_actual_specialty(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    filters: PublicationActualSpecialtyFilter = Depends()
):
    filter_dict = filters.model_dump(exclude_none=True)
    items, total = await publication_service.get_paginated_publication_actual_specialty(db, page, per_page, filter_dict)
    total_pages = ceil(total / per_page)
    return PublicationActualSpecialtyResponse(
        items=[PublicationActualSpecialtyOut.model_validate(obj) for obj in items],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get(
    "/{pub_id}",
    response_model=PublicationResponse,
    dependencies=[Depends(require_role("user"))],
    description="Получает информацию о публикации по её ID. Если публикация не найдена, возвращается ошибка 404."
)
async def get_publication(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        pub = await publication_service.get_publication_by_id(db, pub_id)
        if not pub:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Публикация не найдена")
        return pub
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_publication: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
@router.post(
    "/",
    response_model=PublicationResponse,
    dependencies=[Depends(require_role("admin"))],
    description="Создает новую публикацию. Доступно только администраторам."
)
async def create_publication(data: PublicationCreate, db: AsyncSession = Depends(get_db1_session)):
    return await publication_service.create_publication(db, data)

@router.put(
    "/{pub_id}",
    response_model=PublicationResponse,
    dependencies=[Depends(require_role("admin"))],
    description="Обновляет информацию о публикации по её ID. Если публикация не найдена, возвращается ошибка 404. "
                "Доступно только администраторам."
)
async def update_publication(pub_id: int, data: PublicationUpdate, db: AsyncSession = Depends(get_db1_session)):
    pub = await publication_service.update_publication(db, pub_id, data)
    if not pub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Публикация не найдена")
    return pub

@router.delete(
    "/{pub_id}",
    dependencies=[Depends(require_role("admin"))],
    description="Удаляет публикацию по её ID. Если публикация не найдена, возвращается ошибка 404. "
                "Доступно только администраторам."
)
async def delete_publication(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    await publication_service.delete_publication(db, pub_id)
    return {"detail": "Публикация удалена"}