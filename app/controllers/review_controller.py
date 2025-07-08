from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.review import ReviewOut, ReviewCreate, ReviewUpdate
from app.services import review_service

router = APIRouter()

@router.get("/", response_model=list[ReviewOut],  dependencies=[Depends(require_role("user"))])
async def list_reviews(db: AsyncSession = Depends(get_db1_session)):
    return await review_service.get_all_reviews(db)

@router.get("/{pub_id}", response_model=ReviewOut,  dependencies=[Depends(require_role("user"))])
async def get_review(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    review = await review_service.get_review_by_pub_id(db, pub_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review

@router.post("/", response_model=ReviewOut,  dependencies=[Depends(require_role("admin"))])
async def create_review(data: ReviewCreate, db: AsyncSession = Depends(get_db1_session)):
    return await review_service.create_review(db, data)

@router.put("/{pub_id}", response_model=ReviewOut,  dependencies=[Depends(require_role("admin"))])
async def update_review(pub_id: int, data: ReviewUpdate, db: AsyncSession = Depends(get_db1_session)):
    review = await review_service.update_review(db, pub_id, data)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review

@router.delete("/{pub_id}",  dependencies=[Depends(require_role("admin"))])
async def delete_review(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    await review_service.delete_review(db, pub_id)
    return {"detail": "Review deleted"}
