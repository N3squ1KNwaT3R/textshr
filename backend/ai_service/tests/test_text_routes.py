import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.parametrize("text", ["", "   ", "\t\n"])
async def test_text_correction_empty(client: AsyncClient, text: str):
    response = await client.post("/v1/text/text_correction", json={"text": text})
    assert response.status_code == 422  


async def test_text_correction_too_long(client: AsyncClient):
    long_text = "a" * 10_001
    response = await client.post("/v1/text/text_correction", json={"text": long_text})
    assert response.status_code == 422


async def test_text_correction_valid(client: AsyncClient):
    response = await client.post("/v1/text/text_correction", json={"text": "hello worlt"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "Corrected text here" in data["result"]["text"]

async def test_text_summarization_valid(client: AsyncClient):
    response = await client.post("/v1/text/text_summarization", json={"text": "Long text..."})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "Summarized text here" in data["result"]["text"]

async def test_hello(client: AsyncClient):
    response = await client.post("/v1/text/hello")
    assert response.status_code == 200
    assert response.json() == {"result": "all alright"}