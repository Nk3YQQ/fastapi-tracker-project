import os
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.utils import create_asyncpg_engine

load_dotenv()


@dataclass
class PostgresSettingsSchema:
    driver: str
    user: str
    password: str
    host: str
    db_name: str
    port: int = 5432


POSTGRES_PARAMS = {
    'driver': 'asyncpg',
    'db_name': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
}

engine = create_asyncpg_engine(PostgresSettingsSchema, POSTGRES_PARAMS)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db() -> AsyncSession:
    """ Создаёт шлюз с базой данных """
    async with async_session() as session:
        yield session
