from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role, logger
from app.schemas.index import IndexOut, IndexCreate, IndexUpdate
from app.services import index_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[IndexOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех индексаций публикаций",
    description="Этот эндпоинт возвращает список всех индексаций публикаций из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_indexes(db: AsyncSession = Depends(get_db1_session)):
    try:
        indexes = await index_service.get_all_indexes(db)
        if not indexes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Список индексаций пуст")
        return indexes
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_indexes: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get(
    "/{pub_id}",
    response_model=IndexOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить индексацию по ID публикации",
    description="Этот эндпоинт возвращает информацию об индексации публикации по указанному ID публикации. "
                "Если индексация не найдена, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_index(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    try:
        idx = await index_service.get_index_by_pub_id(db, pub_id)
        if not idx:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Индексация не найдена")
        return idx
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_index: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post(
    "/",
    response_model=IndexOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новую индексацию",
    description="Этот эндпоинт создает новую запись индексации в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_index(data: IndexCreate, db: AsyncSession = Depends(get_db1_session)):
    try:
        return await index_service.create_index(db, data)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in create_index: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put(
    "/{pub_id}",
    response_model=IndexOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить индексацию",
    description="Этот эндпоинт обновляет информацию об индексации по указанному ID публикации. "
                "Если индексация не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_index(pub_id: int, data: IndexUpdate, db: AsyncSession = Depends(get_db1_session)):
    try:
        idx = await index_service.update_index(db, pub_id, data)
        if not idx:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Индексация не найдена")
        return idx
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in update_index: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete(
    "/{pub_id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить индексацию",
    description="Этот эндпоинт удаляет индексацию по указанному ID публикации. "
                "Если индексация не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_index(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        await index_service.delete_index(db, pub_id)
        return {"detail": "Индексация удалена"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in delete_index: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
