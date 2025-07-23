from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.city import CityCreate, CityUpdate, CityOut
from app.services import city_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[CityOut],
    dependencies=[Depends(require_role("user"))],
    summary="Получить список всех городов",
    description="Этот эндпоинт возвращает список всех городов из базы данных. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_cities(db: AsyncSession = Depends(get_db1_session)):
    return await city_service.get_all_cities(db)

@router.get(
    "/{city_id}",
    response_model=CityOut,
    dependencies=[Depends(require_role("user"))],
    summary="Получить информацию о городе по ID",
    description="Этот эндпоинт возвращает информацию о городе по указанному ID. "
                "Если город не найден, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_city(city_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    city = await city_service.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="Город не найден")
    return city

@router.post(
    "/",
    response_model=CityOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Создать новую запись города",
    description="Этот эндпоинт создает новую запись города в базе данных. "
                "Доступ разрешен только администраторам."
)
async def create_city(data: CityCreate, db: AsyncSession = Depends(get_db1_session)):
    return await city_service.create_city(db, data)

@router.put(
    "/{city_id}",
    response_model=CityOut,
    dependencies=[Depends(require_role("admin"))],
    summary="Обновить информацию о городе",
    description="Этот эндпоинт обновляет информацию о городе по указанному ID. "
                "Если город не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_city(city_id: int, data: CityUpdate, db: AsyncSession = Depends(get_db1_session)):
    updated_city = await city_service.update_city(db, city_id, data)
    if not updated_city:
        raise HTTPException(status_code=404, detail="Город не найден")
    return updated_city

@router.delete(
    "/{city_id}",
    dependencies=[Depends(require_role("admin"))],
    summary="Удалить город",
    description="Этот эндпоинт удаляет город по указанному ID. "
                "Если город не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db1_session)):
    success = await city_service.delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=404, detail="Город не найден")
    return {"detail": "Город удален"}