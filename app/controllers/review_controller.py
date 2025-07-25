from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role, logger
from app.schemas.review import ReviewOut, ReviewCreate, ReviewUpdate
from app.services import review_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[ReviewOut],
    dependencies=[Depends(require_role("user"))],
    description="Получает список всех записей о рецензировании. Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def list_reviews(db: AsyncSession = Depends(get_db1_session)):
    return await review_service.get_all_reviews(db)

@router.get(
    "/{pub_id}",
    response_model=ReviewOut,
    dependencies=[Depends(require_role("user"))],
    description="Получает запись о рецензировании по ID публикации. Если запись о рецензировании не найден, возвращается ошибка 404. "
                "Доступ разрешен только пользователям с ролью 'user' и выше."
)
async def get_review(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    try:
        review = await review_service.get_review_by_pub_id(db, pub_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_review: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/",
    response_model=ReviewOut,
    dependencies=[Depends(require_role("admin"))],
    description="Создает новый запись о рецензировании. Доступ разрешен только администраторам."
)
async def create_review(data: ReviewCreate, db: AsyncSession = Depends(get_db1_session)):
    return await review_service.create_review(db, data)

@router.put(
    "/{pub_id}",
    response_model=ReviewOut,
    dependencies=[Depends(require_role("admin"))],
    description="Обновляет запись о рецензировании по ID публикации. Если запись о рецензировании не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def update_review(pub_id: int, data: ReviewUpdate, db: AsyncSession = Depends(get_db1_session)):
    review = await review_service.update_review(db, pub_id, data)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись о рецензировании не найдена")
    return review

@router.delete(
    "/{pub_id}",
    dependencies=[Depends(require_role("admin"))],
    description="Удаляет запись о рецензировании по ID публикации. Если запись о рецензировании не найден, возвращается ошибка 404. "
                "Доступ разрешен только администраторам."
)
async def delete_review(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    await review_service.delete_review(db, pub_id)
    return {"detail": "Запись о рецензировании удалена"}
