import pytest
from schemas.text import TextCreateRequest
from schemas.text import PasswordRequiredResponse


@pytest.mark.asyncio
async def test_password_required(storage_service):
    data = TextCreateRequest(
        text="secret",
        ttl=60,
        only_one_read=False,
        password="1234",
        summary=None
    )

    res = await storage_service.create_text(data, "user1")

    response = await storage_service.get_text(res.key)

    assert isinstance(response, PasswordRequiredResponse)


@pytest.mark.asyncio
async def test_verify_password(storage_service):
    data = TextCreateRequest(
        text="secret",
        ttl=60,
        only_one_read=False,
        password="1234",
        summary=None
    )

    res = await storage_service.create_text(data, "user1")

    text = await storage_service.verify_text_password(res.key, "1234")

    assert text.text == "secret"


@pytest.mark.asyncio
async def test_only_one_read(storage_service):
    data = TextCreateRequest(
        text="once",
        ttl=60,
        only_one_read=True,
        password=None,
        summary=None
    )

    res = await storage_service.create_text(data, "user1")

    first = await storage_service.get_text(res.key)
    assert first.text == "once"

    second = await storage_service.get_text(res.key)
    assert second is None
