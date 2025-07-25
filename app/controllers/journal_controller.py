from math import ceil

from fastapi import APIRouter, Depends, Path, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db1_session
from app.core.security import require_role, logger
from app.schemas.journal import JournalCreate, JournalUpdate, JournalOut, PaginatedJournalResponse, JournalFilter, \
    JournalResponse
from app.services import journal_service

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedJournalResponse,
    dependencies=[Depends(require_role("user"))],
    summary="Получить список журналов (пагинация)",
    description="Этот эндпоинт возвращает список журналов с поддержкой пагинации и фильтрации. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_journals_paginated(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    filters: JournalFilter = Depends()
):
    try:
        filter_dict = filters.model_dump(exclude_none=True)
        items, total = await journal_service.get_paginated_journals(db, page, per_page, filter_dict)
        total_pages = ceil(total / per_page)
        return PaginatedJournalResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_journals_paginated: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get(
    "/{journal_id}",
    response_model=JournalOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить журнал по ID",
    description="Этот эндпоинт возвращает информацию о журнале по указанному ID. "
                "Если журнал не найден, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_journal(journal_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    try:
        journal = await journal_service.get_journal_by_id(db, journal_id)
        if not journal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Журнал не найден")
        return journal
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_journal: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post(
    "/",
    response_model=JournalResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новый журнал",
    description="Этот эндпоинт создает новую запись журнала в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_journal(data: JournalCreate, db: AsyncSession = Depends(get_db1_session)):
    return await journal_service.create_journal(db, data)

@router.put(
    "/{journal_id}",
    response_model=JournalResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить журнал",
    description="Этот эндпоинт обновляет информацию о журнале по указанному ID. "
                "Если журнал не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_journal(journal_id: int, data: JournalUpdate, db: AsyncSession = Depends(get_db1_session)):
    journal = await journal_service.update_journal(db, journal_id, data)
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Журнал не найден")
    return journal

@router.delete(
    "/{journal_id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить журнал",
    description="Этот эндпоинт удаляет журнал по указанному ID. "
                "Если журнал не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_journal(journal_id: int, db: AsyncSession = Depends(get_db1_session)):
    await journal_service.delete_journal(db, journal_id)
    return {"detail": "Журнал удален"}