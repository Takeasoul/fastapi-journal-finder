import json
from math import ceil
from typing import Optional

from fastapi import APIRouter, Depends, Path, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.core.security import require_role
from app.schemas.publication import PublicationOut, PublicationCreate, PublicationUpdate, PaginatedResponse, \
    PublicationFilter
from app.schemas.publication_actual_specialty import PublicationActualSpecialtyOut, PublicationActualSpecialtyFilter
from app.schemas.publication_base_info import PublicationBaseInfoOut, PaginatedBaseInfoResponse, \
    PublicationBaseInfoFilter
from app.services import publication_service

router = APIRouter()

@router.get("/", response_model=PaginatedResponse,  dependencies=[Depends(require_role("user"))], description="ВАЖНО: из-за бага Swagger параметр languages нужно передавать через query (?languages=русский&languages=английский), а не через body, даже если Swagger предлагает body.")
async def list_publications_paginated(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    filters: PublicationFilter = Depends()
):
    filter_dict = filters.model_dump(exclude_none=True)
    publications, total = await publication_service.get_paginated_publications(db, page, per_page, filter_dict)
    total_pages = ceil(total / per_page)
    return PaginatedResponse(
        items=publications,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/getallwithbaseinfo", response_model=PaginatedBaseInfoResponse,  dependencies=[Depends(require_role("user"))], description="ВАЖНО: из-за бага Swagger параметр languages нужно передавать через query (?languages=русский&languages=английский), а не через body, даже если Swagger предлагает body.")
async def list_publication_base_info(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    filters: PublicationBaseInfoFilter = Depends()
):
    filter_dict = filters.model_dump(exclude_none=True)
    items, total = await publication_service.get_paginated_publication_base_info(db, page, per_page, filter_dict)
    total_pages = ceil(total / per_page)
    return PaginatedBaseInfoResponse(
        items=[PublicationBaseInfoOut.model_validate(obj) for obj in items],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/getallwithactualspecialty", response_model=PaginatedResponse,  dependencies=[Depends(require_role("user"))])
async def list_publication_actual_specialty(
    db: AsyncSession = Depends(get_db1_session),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    filters: PublicationActualSpecialtyFilter = Depends()
):
    filter_dict = filters.model_dump(exclude_none=True)
    items, total = await publication_service.get_paginated_publication_actual_specialty(db, page, per_page, filter_dict)
    total_pages = ceil(total / per_page)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/{pub_id}", response_model=PublicationOut,  dependencies=[Depends(require_role("user"))])
async def get_publication(pub_id: int = Path(...), db: AsyncSession = Depends(get_db1_session)):
    pub = await publication_service.get_publication_by_id(db, pub_id)
    if not pub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found")
    return pub

@router.post("/", response_model=PublicationOut,  dependencies=[Depends(require_role("admin"))])
async def create_publication(data: PublicationCreate, db: AsyncSession = Depends(get_db1_session)):
    return await publication_service.create_publication(db, data)

@router.put("/{pub_id}", response_model=PublicationOut,  dependencies=[Depends(require_role("admin"))])
async def update_publication(pub_id: int, data: PublicationUpdate, db: AsyncSession = Depends(get_db1_session)):
    pub = await publication_service.update_publication(db, pub_id, data)
    if not pub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found")
    return pub

@router.delete("/{pub_id}",  dependencies=[Depends(require_role("admin"))])
async def delete_publication(pub_id: int, db: AsyncSession = Depends(get_db1_session)):
    await publication_service.delete_publication(db, pub_id)
    return {"detail": "Publication deleted"}