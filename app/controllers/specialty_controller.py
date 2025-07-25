from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.specialty import SpecialtyCreate, SpecialtyUpdate, SpecialtyOut, SpecialtyResponse
from app.services import specialty_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[SpecialtyOut],
    dependencies=[Depends(require_role("user"))],
    description="Получает список всех специальностей. Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_specialties(db: AsyncSession = Depends(get_db1_session)):
    return await specialty_service.get_all_specialties(db)

@router.get(
    "/{specialty_id}",
    response_model=SpecialtyOut,
    dependencies=[Depends(require_role("user"))],
    description="Получает специальность по её ID. Если специальность не найдена, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_specialty(specialty_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await specialty_service.get_specialty_by_id(db, specialty_id)

@router.post(
    "/",
    response_model=SpecialtyResponse,
    dependencies=[Depends(require_role("admin"))],
    description="Создает новую специальность. Доступ разрешен только администраторам."
)
async def create_specialty(data: SpecialtyCreate, db: AsyncSession = Depends(get_db1_session)):
    return await specialty_service.create_specialty(db, data)

@router.put(
    "/{specialty_id}",
    response_model=SpecialtyResponse,
    dependencies=[Depends(require_role("admin"))],
    description="Обновляет специальность по её ID. Если специальность не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_specialty(specialty_id: int, data: SpecialtyUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await specialty_service.update_specialty(db, specialty_id, data)

@router.delete(
    "/{specialty_id}",
    dependencies=[Depends(require_role("admin"))],
    description="Удаляет специальность по её ID. Если специальность не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_specialty(specialty_id: int, db: AsyncSession = Depends(get_db1_session)):
    await specialty_service.delete_specialty(db, specialty_id)
    return {"detail": "Специальность удалена"}