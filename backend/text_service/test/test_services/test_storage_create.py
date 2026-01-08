import pytest
from schemas.text import TextCreateRequest


@pytest.mark.asyncio
async def test_create_small_text(storage_service):
    data = TextCreateRequest(
        text="hello world",
        ttl=60,
        only_one_read=False,
        password=None,
        summary=None
    )

    res = await storage_service.create_text(data, creator="user1")

    assert res.key is not None
    assert len(res.key) > 0


@pytest.mark.asyncio
async def test_create_large_text(storage_service):
    big_text = "a" * 20000

    data = TextCreateRequest(
        text=big_text,
        ttl=60,
        only_one_read=False,
        password=None,
        summary=None
    )

    res = await storage_service.create_text(data, creator="user1")

    assert res.key
