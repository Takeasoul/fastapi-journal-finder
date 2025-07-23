from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.edu_level import (
    EduLevelOut,
    EduLevelCreate,
    EduLevelUpdate
)
from app.services import edu_level_service

router = APIRouter()


@router.get(
    "/",
    response_model=list[EduLevelOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех уровней образования",
    description="Этот эндпоинт возвращает список всех уровней образования из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_edu_levels(db: AsyncSession = Depends(get_db1_session)):
    return await edu_level_service.get_all_edu_levels(db)


@router.get(
    "/{edu_level_id}",
    response_model=EduLevelOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить уровень образования по ID",
    description="Этот эндпоинт возвращает информацию об уровне образования по указанному ID. "
                "Если уровень образования не найден, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_edu_level(edu_level_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    edu_level = await edu_level_service.get_edu_level_by_id(db, edu_level_id)
    if not edu_level:
        raise HTTPException(status_code=404, detail="Уровень образования не найден")
    return edu_level


@router.post(
    "/",
    response_model=EduLevelOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новый уровень образования",
    description="Этот эндпоинт создает новую запись уровня образования в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_edu_level(data: EduLevelCreate, db: AsyncSession = Depends(get_db1_session)):
    return await edu_level_service.create_edu_level(db, data)


@router.put(
    "/{edu_level_id}",
    response_model=EduLevelOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить уровень образования",
    description="Этот эндпоинт обновляет информацию об уровне образования по указанному ID. "
                "Если уровень образования не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_edu_level(edu_level_id: int, data: EduLevelUpdate, db: AsyncSession = Depends(get_db1_session)):
    updated_edu_level = await edu_level_service.update_edu_level(db, edu_level_id, data)
    if not updated_edu_level:
        raise HTTPException(status_code=404, detail="Уровень образования не найден")
    return updated_edu_level


@router.delete(
    "/{edu_level_id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить уровень образования",
    description="Этот эндпоинт удаляет уровень образования по указанному ID. "
                "Если уровень образования не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_edu_level(edu_level_id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await edu_level_service.delete_edu_level(db, edu_level_id)
    if not success:
        raise HTTPException(status_code=404, detail="Уровень образования не найден")
    return {"detail": "Уровень образования удален"}