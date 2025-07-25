from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut, ContactResponse
from app.services import contact_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[ContactOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех контактных информаций",
    description="Этот эндпоинт возвращает список всех контактных информаций из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_contacts(db: AsyncSession = Depends(get_db1_session)):
    try:
        contacts = await contact_service.get_all_contacts(db)
        if not contacts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Список контактных информаций пуст")
        return contacts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/{pub_id}",
    response_model=ContactOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить контактную информацию по ID публикации",
    description="Этот эндпоинт возвращает информацию о контактной информации по указанному ID публикации. "
                "Если контактная информация не найдена, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_contact(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    try:
        contact = await contact_service.get_contact_by_pub_id(db, pub_id)
        return contact
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/",
    response_model=ContactResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новую контактную информацию",
    description="Этот эндпоинт создает новую запись контактной информации в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_contact( data: ContactCreate, db: AsyncSession = Depends(get_db1_session)):
    try:
        contact = await contact_service.create_contact(db, data)
        return contact
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put(
    "/{pub_id}",
    response_model=ContactResponse,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить контактную информацию",
    description="Этот эндпоинт обновляет информацию о контактной информации по указанному ID публикации. "
                "Если контактная информация не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_contact(pub_id: int, data: ContactUpdate, db: AsyncSession = Depends(get_db1_session)):
    try:
        updated_contact = await contact_service.update_contact(db, pub_id, data)
        return updated_contact
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete(
    "/{pub_id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить контактную информацию",
    description="Этот эндпоинт удаляет контактную информацию по указанному ID публикации. "
                "Если контактная информация не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_contact(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        success = await contact_service.delete_contact(db, pub_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контактная информация не найдена")
        return {"detail": "Контактная информация удалена"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
