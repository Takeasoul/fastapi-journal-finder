from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.IPWhitelist import IPWhitelist
import ipaddress

class IPWhitelistService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_ip_whitelist(self, ip_network: str, organization_name: str = None) -> IPWhitelist:
        try:
            # Проверяем корректность IP-сети
            ipaddress.ip_network(ip_network)
        except ValueError:
            raise ValueError("Некорректный формат IP-сети")

        # Проверяем, существует ли уже такая запись
        result = await self.db.execute(select(IPWhitelist).where(IPWhitelist.ip_network == ip_network))
        if result.scalar_one_or_none():
            raise ValueError("Такая IP-сеть уже существует")

        # Создаем новую запись
        new_entry = IPWhitelist(ip_network=ip_network, organization_name=organization_name)
        self.db.add(new_entry)
        await self.db.commit()
        await self.db.refresh(new_entry)
        return new_entry

    async def delete_ip_whitelist(self, ip_network: str) -> bool:
        result = await self.db.execute(select(IPWhitelist).where(IPWhitelist.ip_network == ip_network))
        entry = result.scalar_one_or_none()

        if not entry:
            raise ValueError("Запись с такой IP-сетью не найдена")

        await self.db.delete(entry)
        await self.db.commit()
        return True

    async def update_ip_whitelist(self, ip_network: str, new_organization_name: str) -> IPWhitelist:
        result = await self.db.execute(select(IPWhitelist).where(IPWhitelist.ip_network == ip_network))
        entry = result.scalar_one_or_none()

        if not entry:
            raise ValueError("Запись с такой IP-сетью не найдена")

        entry.organization_name = new_organization_name
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def get_all_ip_whitelists(self) -> list[IPWhitelist]:
        result = await self.db.execute(select(IPWhitelist))
        return list(result.scalars().all())