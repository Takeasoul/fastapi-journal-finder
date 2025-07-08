import logging
from alembic import command
from alembic.config import Config
from app.core.database import db1_engine
from app.core.base import Base
from app import models
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

async def init_db():
    # Инициализация первой базы данных
    async with db1_engine.begin() as conn:
        logger.info("Creating tables in DB1...")
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        logger.info("Tables created in DB1")



@asynccontextmanager
async def lifespan(app):
    logger.info("Starting migrations...")
    logger.info("Migrations complete.")

    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized.")

    yield
    logger.info("Application shutdown.")
