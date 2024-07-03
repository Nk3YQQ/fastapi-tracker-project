import os
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database import get_db
from src.main import app
from src.models import Base
from src.settings import EMPLOYEE_DATA_PATH, TASKS_DATA_PATH
from src.utils import open_json_file

load_dotenv()

driver = 'asyncpg'
db_name = os.getenv('POSTGRES_TEST_DB')
user = os.getenv('POSTGRES_TEST_USER')
password = os.getenv('POSTGRES_TEST_PASSWORD')
host = os.getenv('POSTGRES_TEST_HOST')

DATABASE_URL = f"postgresql+{driver}://{user}:{password}@{host}:5432/{db_name}"

engine = create_async_engine(url=DATABASE_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncSession, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client


@pytest.fixture()
def employee_list() -> list[dict]:
    return open_json_file(EMPLOYEE_DATA_PATH)


@pytest.fixture()
def tasks_list() -> list[dict]:
    return open_json_file(TASKS_DATA_PATH)


@pytest.fixture()
def employee_payload_updated() -> dict:
    return {
        "first_name": "Anton",
        "last_name": "Antonov",
        "email": "anton.antonov@mail.ru",
        "title": "Java-developer",
        "birth_date": "1997-04-24"
    }


@pytest.fixture()
def task_payload_updated() -> dict:
    return {
        "title": "Analyze app working",
        "status": "received",
        "employee_id": 4
    }
