from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from collections.abc import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.core.config import settings

# Строки подключения для двух баз данных
SQLALCHEMY_DB1_URL = (
    f"mysql+aiomysql://{settings.DB1_USER}:{settings.DB1_PASSWORD}"
    f"@{settings.DB1_HOST}:{settings.DB1_PORT}/{settings.DB1_NAME}"
)
# Асинхронные движки для каждой базы данных
db1_engine = create_async_engine(SQLALCHEMY_DB1_URL, echo=True, future=True, pool_pre_ping=True, pool_recycle=1800)

# Фабрики сессий для каждой базы данных
db1_session = async_sessionmaker(
    bind=db1_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Генераторы сессий
async def get_db1_session() -> AsyncGenerator[AsyncSession, None]:
    async with db1_session() as session:
        yield session
