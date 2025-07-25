from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db1_session
from app.core.security import require_role, logger
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
    try:
        edu_levels = await edu_level_service.get_all_edu_levels(db)
        if not edu_levels:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Список уровней образования пуст")
        return edu_levels
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_edu_levels: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
    try:
        return await edu_level_service.get_edu_level_by_id(db, edu_level_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_edu_level: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post(
    "/",
    response_model=EduLevelOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новый уровень образования",
    description="Этот эндпоинт создает новую запись уровня образования в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_edu_level(data: EduLevelCreate, db: AsyncSession = Depends(get_db1_session)):
    try:
        return await edu_level_service.create_edu_level(db, data)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in create_edu_level: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
    try:
        updated_edu_level = await edu_level_service.update_edu_level(db, edu_level_id, data)
        if not updated_edu_level:
            raise HTTPException(status_code=404, detail="Уровень образования не найден")
        return updated_edu_level
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in update_edu_level: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete(
    "/{edu_level_id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить уровень образования",
    description="Этот эндпоинт удаляет уровень образования по указанному ID. "
                "Если уровень образования не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_edu_level(edu_level_id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        success = await edu_level_service.delete_edu_level(db, edu_level_id)
        if not success:
            raise HTTPException(status_code=404, detail="Уровень образования не найден")
        return {"detail": "Уровень образования удален"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in delete_edu_level: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")