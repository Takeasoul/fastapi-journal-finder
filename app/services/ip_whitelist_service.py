from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import logger
from app.models.IPWhitelist import IPWhitelist
import ipaddress

from app.schemas.ip_whitelist import IPWhitelistUpdate


class IPWhitelistService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_ip_whitelist(self, ip_network: str, organization_name: str = None) -> IPWhitelist:
        logger.debug(f"Received ip_network: {ip_network}, organization_name: {organization_name}")

        # Проверяем корректность IP-сети
        try:
            ip_network_obj = ipaddress.ip_network(ip_network, strict=False)
        except ValueError as e:
            logger.error(f"Validation failed for ip_network: {ip_network}. Error: {e}")
            raise ValueError("Некорректный формат IP-сети")

        # Проверяем, существует ли уже такая запись
        result = await self.db.execute(select(IPWhitelist).where(IPWhitelist.ip_network == ip_network))
        if result.scalar_one_or_none():
            raise ValueError("Такая IP-сеть уже существует")

        # Создаем новую запись
        new_entry = IPWhitelist(ip_network=str(ip_network_obj), organization_name=organization_name)
        self.db.add(new_entry)
        await self.db.commit()
        await self.db.refresh(new_entry)
        return new_entry

    async def delete_ip_whitelist(self, id: int) -> bool:
        result = await self.db.execute(select(IPWhitelist).where(IPWhitelist.id == id))
        entry = result.scalar_one_or_none()

        if not entry:
            raise ValueError("Запись с такой IP-сетью не найдена")

        await self.db.delete(entry)
        await self.db.commit()
        return True

    async def update_ip_whitelist(self, id: int, new_data: IPWhitelistUpdate) -> IPWhitelist:
        # Поиск записи по ID
        result = await self.db.execute(select(IPWhitelist).where(IPWhitelist.id == id))
        entry = result.scalar_one_or_none()

        if not entry:
            raise ValueError("Запись с таким ID не найдена")

        # Обновление полей
        if new_data.ip_network is not None:
            try:
                normalized_ip_network = self.normalize_ip_network(new_data.ip_network)
                entry.ip_network = normalized_ip_network
            except ValueError as e:
                raise ValueError(f"Ошибка при обновлении ip_network: {e}")

        if new_data.organization_name is not None:
            entry.organization_name = new_data.organization_name

        # Сохранение изменений
        await self.db.commit()
        await self.db.refresh(entry)
        return entry


    async def get_all_ip_whitelists(self) -> list[IPWhitelist]:
        result = await self.db.execute(select(IPWhitelist))
        return list(result.scalars().all())

    @staticmethod
    def normalize_ip_network(ip_network: str) -> str:
        """
        Нормализует IP-сеть, проверяя её корректность.
        """
        try:
            network = ipaddress.ip_network(ip_network, strict=False)
            return str(network)
        except ValueError as e:
            raise ValueError(f"Некорректный формат IP-сети: {e}")