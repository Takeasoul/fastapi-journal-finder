import ipaddress
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.IPWhitelist import IPWhitelist


async def is_ip_whitelisted(db: AsyncSession, client_ip: str) -> bool:
    try:
        ip = ipaddress.ip_address(client_ip)
    except ValueError:
        return False  # IP-адрес некорректен

    result = await db.execute(select(IPWhitelist))
    entries = result.scalars().all()

    for entry in entries:
        try:
            network = ipaddress.ip_network(entry.ip_network)
            if ip in network:
                return True
        except ValueError:
            continue  # Игнорируем некорректные записи

    return False
