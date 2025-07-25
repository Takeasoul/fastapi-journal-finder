from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db1_session
from app.core.security import require_role, logger
from app.schemas.grnti import GrntiCreate, GrntiUpdate, GrntiOut
from app.services import grnti_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[GrntiOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех ГРНТИ",
    description="Этот эндпоинт возвращает список всех записей ГРНТИ из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_grnti(db: AsyncSession = Depends(get_db1_session)):
    try:
        grnti_list = await grnti_service.get_all_grnti(db)
        if not grnti_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Список ГРНТИ пуст")
        return grnti_list
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_grnti: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get(
    "/{grnti_id}",
    response_model=GrntiOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить запись ГРНТИ по ID",
    description="Этот эндпоинт возвращает информацию о записи ГРНТИ по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_grnti(grnti_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    try:
        return await grnti_service.get_grnti_by_id(db, grnti_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_grnti: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post(
    "/",
    response_model=GrntiOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новую запись ГРНТИ",
    description="Этот эндпоинт создает новую запись ГРНТИ в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_grnti(data: GrntiCreate, db: AsyncSession = Depends(get_db1_session)):
    try:
        return await grnti_service.create_grnti(db, data)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in create_grnti: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put(
    "/{grnti_id}",
    response_model=GrntiOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить запись ГРНТИ",
    description="Этот эндпоинт обновляет информацию о записи ГРНТИ по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_grnti(grnti_id: int, data: GrntiUpdate, db: AsyncSession = Depends(get_db1_session)):
    try:
        updated_grnti = await grnti_service.update_grnti(db, grnti_id, data)
        if not updated_grnti:
            raise HTTPException(status_code=404, detail="ГРНТИ не найден")
        return updated_grnti
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in update_grnti: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete(
    "/{grnti_id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить запись ГРНТИ",
    description="Этот эндпоинт удаляет запись ГРНТИ по указанному ID. "
                "Если запись не найдена, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_grnti(grnti_id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        success = await grnti_service.delete_grnti(db, grnti_id)
        if not success:
            raise HTTPException(status_code=404, detail="ГРНТИ не найден")
        return {"detail": "ГРНТИ удален"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in delete_grnti: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
