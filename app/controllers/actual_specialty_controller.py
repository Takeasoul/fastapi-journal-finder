from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.actual_specialty import ActualSpecialtyCreate, ActualSpecialtyUpdate, ActualSpecialtyOut
from app.services import actual_specialty_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[ActualSpecialtyOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех актуальных специальностей",
    description="Этот эндпоинт возвращает список всех записей актуальных специальностей из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_actual_specialties(db: AsyncSession = Depends(get_db1_session)):
    return await actual_specialty_service.get_all_actual_specialties(db)

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
        raise HTTPException(status_code=404, detail="Не найдена актуальная специальность")
    return record

@router.post(
    "/",
    response_model=ActualSpecialtyOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новую запись актуальной специальности",
    description="Этот эндпоинт создает новую запись актуальной специальности в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_actual_specialty(data: ActualSpecialtyCreate, db: AsyncSession = Depends(get_db1_session)):
    return await actual_specialty_service.create_actual_specialty(db, data)

@router.put(
    "/{id}",
    response_model=ActualSpecialtyOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить запись актуальной специальности",
    description="Этот эндпоинт обновляет существующую запись актуальной специальности по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_actual_specialty(id: int, data: ActualSpecialtyUpdate, db: AsyncSession = Depends(get_db1_session)):
    record = await actual_specialty_service.update_actual_specialty(db, id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Не найдена актуальная специальность")
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
        raise HTTPException(status_code=404, detail="Не найдена актуальная специальность")
    return {"detail": "Актуальная специальность удалена"}
