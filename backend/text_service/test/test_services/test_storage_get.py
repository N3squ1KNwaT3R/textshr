import pytest
from schemas.text import TextCreateRequest


@pytest.mark.asyncio
async def test_get_text(storage_service):
    create = TextCreateRequest(
        text="hello",
        ttl=60,
        only_one_read=False,
        password=None,
        summary="test"
    )

    res = await storage_service.create_text(create, "user1")

    text = await storage_service.get_text(res.key)

    assert text.text == "hello"
    assert text.summary == "test"
