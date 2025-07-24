from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db1_session
from app.schemas.ip_whitelist import IPWhitelistCreate, IPWhitelistUpdate, IPWhitelistResponse
from app.services.ip_whitelist_service import IPWhitelistService
from typing import List
from app.models.IPWhitelist import IPWhitelist

router = APIRouter()

@router.post("/ip-whitelist", summary="Добавить IP-сеть в whitelist")
async def add_ip_whitelist(
    data: IPWhitelistCreate,
    db: AsyncSession = Depends(get_db1_session)
):
    service = IPWhitelistService(db)
    try:
        entry = await service.add_ip_whitelist(data.ip_network, data.organization_name)
        return {"message": "Запись добавлена", "entry": entry}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/ip-whitelist/{ip_network}", summary="Удалить IP-сеть из whitelist")
async def delete_ip_whitelist(
    ip_network: str,
    db: AsyncSession = Depends(get_db1_session)
):
    service = IPWhitelistService(db)
    try:
        success = await service.delete_ip_whitelist(ip_network)
        if success:
            return {"message": "Запись удалена"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/ip-whitelist/{ip_network}", summary="Обновить запись в whitelist")
async def update_ip_whitelist(
    ip_network: str,
    data: IPWhitelistUpdate,
    db: AsyncSession = Depends(get_db1_session)
):
    service = IPWhitelistService(db)
    try:
        entry = await service.update_ip_whitelist(ip_network, data.organization_name)
        return {"message": "Запись обновлена", "entry": entry}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/ip-whitelist", summary="Получить все записи whitelist", response_model=List[IPWhitelistResponse])
async def get_all_ip_whitelists(
    db: AsyncSession = Depends(get_db1_session)
) -> List[IPWhitelistResponse]:
    service = IPWhitelistService(db)
    entries = await service.get_all_ip_whitelists()
    return entries