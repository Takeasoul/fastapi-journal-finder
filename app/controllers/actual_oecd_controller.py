from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.actual_oecd import ActualOECDCreate, ActualOECDUpdate, ActualOECDOut
from app.services import actual_oecd_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[ActualOECDOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех актуальных OECD",
    description="Этот эндпоинт возвращает список всех записей актуальных OECD из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_actual_oecd(db: AsyncSession = Depends(get_db1_session)):
    return await actual_oecd_service.get_all_actual_oecd(db)

@router.get(
    "/{id}",
    response_model=ActualOECDOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить запись актуального OECD по ID",
    description="Этот эндпоинт возвращает запись актуального OECD по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_actual_oecd(actual_oecd_id: int, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_oecd_service.get_actual_oecd_by_id(db, actual_oecd_id)
    if not record:
        raise HTTPException(status_code=404, detail="Не найден актуальный ОЕСД")
    return record

@router.post(
    "/",
    response_model=ActualOECDOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новую запись актуального OECD",
    description="Этот эндпоинт создает новую запись актуального OECD в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_actual_oecd(data: ActualOECDCreate, db: AsyncSession = Depends(get_db1_session)):
    return await actual_oecd_service.create_actual_oecd(db, data)

@router.put(
    "/{id}",
    response_model=ActualOECDOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить запись актуального OECD",
    description="Этот эндпоинт обновляет существующую запись актуального OECD по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_actual_oecd(actual_oecd_id: int, data: ActualOECDUpdate, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_oecd_service.update_actual_oecd(db, actual_oecd_id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Не найден актуальный ОЕСД")
    return record

@router.delete(
    "/{id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить запись актуального OECD",
    description="Этот эндпоинт удаляет запись актуального OECD по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_actual_oecd(actual_oecd_id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await actual_oecd_service.delete_actual_oecd(db, actual_oecd_id)
    if not success:
        raise HTTPException(status_code=404, detail="Не найден актуальный ОЕСД")
    return {"detail": "Не найден актуальный ОЕСД"}
