import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from page_analyzer import app
from page_analyzer.db import engine


@pytest.fixture(autouse=True)
async def clean_database():
    async with engine.begin() as connection:
        await connection.execute(text("TRUNCATE urls RESTART IDENTITY CASCADE"))


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as http_client:
        yield http_client


@pytest.fixture
async def count_checks():
    async def count() -> int:
        async with engine.begin() as connection:
            result = await connection.execute(text("SELECT count(*) FROM url_checks"))
            return result.scalar_one()

    return count
