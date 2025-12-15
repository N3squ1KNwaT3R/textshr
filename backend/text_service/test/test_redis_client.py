import json
import pytest
from unittest.mock import AsyncMock, patch

from backend.text_service.clients.redis_client import RedisClient


@pytest.fixture
def redis_mock():
    mock = AsyncMock()
    mock.connection_pool = AsyncMock()
    return mock


@pytest.fixture
def client(redis_mock):
    # Патчимо create_redis_client, щоб RedisClient використовував мок
    with patch("backend.text_service.clients.redis_client.create_redis_client", return_value=redis_mock):
        yield RedisClient()


@pytest.mark.asyncio
async def test_set_success(client, redis_mock):
    redis_mock.set.return_value = True
    await client.set("key1", {"a": 1}, ttl=60)
    redis_mock.set.assert_awaited_once_with(
        name="key1", value=json.dumps({"a": 1}), ex=60
    )


@pytest.mark.asyncio
async def test_get_success(client, redis_mock):
    redis_mock.get.return_value = json.dumps({"x": 123})
    result = await client.get("key2")
    redis_mock.get.assert_awaited_once_with("key2")
    assert result == {"x": 123}


@pytest.mark.asyncio
async def test_get_error(client, redis_mock):
    redis_mock.get.side_effect = Exception("Redis error")
    with pytest.raises(Exception):
        await client.get("key2")


@pytest.mark.asyncio
async def test_update_existing_key(client, redis_mock):
    redis_mock.exists.return_value = True
    redis_mock.delete.return_value = True
    redis_mock.set.return_value = True

    result = await client.update("key3", {"val": 1}, ttl=30)
    redis_mock.exists.assert_awaited_once_with("key3")
    redis_mock.delete.assert_awaited_once_with("key3")
    redis_mock.set.assert_awaited_once_with(
        name="key3", value=json.dumps({"val": 1}), ex=30
    )
    assert result is True


@pytest.mark.asyncio
async def test_update_nonexistent_key(client, redis_mock):
    redis_mock.exists.return_value = False
    result = await client.update("key4", {"val": 1}, ttl=30)
    redis_mock.exists.assert_awaited_once_with("key4")
    assert result is False


@pytest.mark.asyncio
async def test_delete_existing_key(client, redis_mock):
    redis_mock.exists.return_value = True
    redis_mock.delete.return_value = True

    result = await client.delete("key5")
    redis_mock.exists.assert_awaited_once_with("key5")
    redis_mock.delete.assert_awaited_once_with("key5")
    assert result is True


@pytest.mark.asyncio
async def test_delete_nonexistent_key(client, redis_mock):
    redis_mock.exists.return_value = False
    result = await client.delete("key6")
    redis_mock.exists.assert_awaited_once_with("key6")
    assert result is False


@pytest.mark.asyncio
async def test_ping_success(client, redis_mock):
    redis_mock.ping.return_value = "PONG"
    result = await client.ping()
    redis_mock.ping.assert_awaited_once()
    assert result is True


@pytest.mark.asyncio
async def test_ping_fail(client, redis_mock):
    redis_mock.ping.side_effect = Exception("Ping failed")
    result = await client.ping()
    assert result is False


@pytest.mark.asyncio
async def test_close(client, redis_mock):
    await client.close()
    redis_mock.close.assert_awaited_once()
    redis_mock.connection_pool.disconnect.assert_awaited_once()
