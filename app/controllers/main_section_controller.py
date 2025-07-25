from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db1_session
from app.core.security import require_role, logger
from app.schemas.main_section import MainSectionCreate, MainSectionUpdate, MainSectionOut, MainSectionResponse
from app.services import main_section_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[MainSectionOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех основных разделов",
    description="Этот эндпоинт возвращает список всех основных разделов из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_main_sections(db: AsyncSession = Depends(get_db1_session)):
    try:
        main_sections = await main_section_service.get_all_main_sections(db)
        if not main_sections:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Список основных разделов пуст")
        return main_sections
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in list_main_sections: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get(
    "/{id}",
    response_model=MainSectionOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить основной раздел по ID",
    description="Этот эндпоинт возвращает информацию об основном разделе по указанному ID. "
                "Если раздел не найден, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_main_section(id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        record = await main_section_service.get_main_section_by_id(db, id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Основной раздел не найден")
        return record
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_main_section: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post(
    "/",
    response_model=MainSectionResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новый основной раздел",
    description="Этот эндпоинт создает новую запись основного раздела в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_main_section(data: MainSectionCreate, db: AsyncSession = Depends(get_db1_session)):
    try:
        return await main_section_service.create_main_section(db, data)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in create_main_section: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put(
    "/{id}",
    response_model=MainSectionResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить основной раздел",
    description="Этот эндпоинт обновляет информацию об основном разделе по указанному ID. "
                "Если раздел не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_main_section(id: int, data: MainSectionUpdate, db: AsyncSession = Depends(get_db1_session)):
    try:
        record = await main_section_service.update_main_section(db, id, data)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Основной раздел не найден")
        return record
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in update_main_section: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete(
    "/{id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить основной раздел",
    description="Этот эндпоинт удаляет основной раздел по указанному ID. "
                "Если раздел не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_main_section(id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        success = await main_section_service.delete_main_section(db, id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Основной раздел не найден")
        return {"detail": "Основной раздел удален"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in delete_main_section: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
