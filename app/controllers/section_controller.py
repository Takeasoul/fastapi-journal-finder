from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.section import SectionCreate, SectionUpdate, SectionOut
from app.services import section_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[SectionOut],
    dependencies=[Depends(require_role("user"))],
    description="Получает список всех разделов. Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_sections(db: AsyncSession = Depends(get_db1_session)):
    return await section_service.get_all_sections(db)

@router.get(
    "/{section_id}",
    response_model=SectionOut,
    dependencies=[Depends(require_role("user"))],
    description="Получает раздел по его ID. Если раздел не найден, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_section(section_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    return await section_service.get_section_by_id(db, section_id)

@router.post(
    "/",
    response_model=SectionOut,
    dependencies=[Depends(require_role("admin"))],
    description="Создает новый раздел. Доступ разрешен только администраторам."
)
async def create_section(data: SectionCreate, db: AsyncSession = Depends(get_db1_session)):
    return await section_service.create_section(db, data)

@router.put(
    "/{section_id}",
    response_model=SectionOut,
    dependencies=[Depends(require_role("admin"))],
    description="Обновляет раздел по его ID. Если раздел не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_section(section_id: int, data: SectionUpdate, db: AsyncSession = Depends(get_db1_session)):
    return await section_service.update_section(db, section_id, data)

@router.delete(
    "/{section_id}",
    dependencies=[Depends(require_role("admin"))],
    description="Удаляет раздел по его ID. Если раздел не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_section(section_id: int, db: AsyncSession = Depends(get_db1_session)):
    await section_service.delete_section(db, section_id)
    return {"detail": "Раздел удален"}