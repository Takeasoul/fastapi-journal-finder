from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

async def get_all_reviews(db: AsyncSession):
    result = await db.execute(select(Review))
    return result.scalars().all()

async def get_review_by_pub_id(db: AsyncSession, pub_id: int):
    result = await db.execute(select(Review).where(Review.pub_id == pub_id))
    return result.scalar_one_or_none()

async def create_review(db: AsyncSession, data: ReviewCreate):
    review = Review(**data.dict())
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

async def update_review(db: AsyncSession, pub_id: int, data: ReviewUpdate):
    review = await get_review_by_pub_id(db, pub_id)
    if review:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(review, key, value)
        await db.commit()
        await db.refresh(review)
    return review

async def delete_review(db: AsyncSession, pub_id: int):
    review = await get_review_by_pub_id(db, pub_id)
    if review:
        await db.delete(review)
        await db.commit()
