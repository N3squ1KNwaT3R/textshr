import pytest
from schemas.text import TextCreateRequest


@pytest.mark.asyncio
async def test_delete_text(storage_service):
    data = TextCreateRequest(
        text="bye",
        ttl=60,
        only_one_read=False,
        password=None,
        summary=None
    )

    res = await storage_service.create_text(data, "user1")

    deleted = await storage_service.delete_text(res.key, "user1")
    assert deleted

    missing = await storage_service.get_text(res.key)
    assert missing is None
