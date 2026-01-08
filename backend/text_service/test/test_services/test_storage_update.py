import pytest
from schemas.text import TextCreateRequest, TextUpdateRequest


@pytest.mark.asyncio
async def test_update_text(storage_service):
    create = TextCreateRequest(
        text="old",
        ttl=60,
        only_one_read=False,
        password=None,
        summary=None
    )

    res = await storage_service.create_text(create, "user1")

    update = TextUpdateRequest(
        text="new",
        ttl=60,
        only_one_read=False,
        password=None,
        summary=None
    )

    ok = await storage_service.update_text(res.key, update, "user1")
    assert ok

    updated = await storage_service.get_text(res.key)
    assert updated.text == "new"
