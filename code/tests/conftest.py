import pytest
from httpx import ASGITransport, AsyncClient

from page_analyzer import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as http_client:
        yield http_client
