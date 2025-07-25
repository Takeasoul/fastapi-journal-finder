from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.logger import logger
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

async def get_all_reviews(db: AsyncSession):
    try:
        result = await db.execute(select(Review))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_review_by_pub_id(db: AsyncSession, pub_id: int):
    result = await db.execute(select(Review).where(Review.pub_id == pub_id))
    return result.scalar_one_or_none()

async def create_review(db: AsyncSession, data: ReviewCreate):
    try:
        review = Review(**data.dict())
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e.errors()}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Duplicate entry or invalid data.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_review(db: AsyncSession, pub_id: int, data: ReviewUpdate):
    try:
        review = await get_review_by_pub_id(db, pub_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(review, key, value)
        await db.commit()
        await db.refresh(review)
        return review
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e.errors()}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid data or duplicate entry.")
    except SQLAlchemyError as e:
        logger.error(f"Database error updating review with pub_id={pub_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error updating review with pub_id={pub_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_review(db: AsyncSession, pub_id: int):
    try:
        review = await get_review_by_pub_id(db, pub_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        await db.delete(review)
        await db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error deleting review with pub_id={pub_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error deleting review with pub_id={pub_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
