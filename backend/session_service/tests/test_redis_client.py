import json
import pytest
import unittest.mock
from client.redis_client import RedisClient


@pytest.fixture
def mock_redis_client():
    mock = unittest.mock.AsyncMock()
    mock.set = unittest.mock.AsyncMock()
    mock.get = unittest.mock.AsyncMock()
    mock.delete = unittest.mock.AsyncMock()
    mock.exists = unittest.mock.AsyncMock()
    mock.close = unittest.mock.AsyncMock()
    return mock


@pytest.fixture
def redis_client(mock_redis_client):
    return RedisClient(client=mock_redis_client)


@pytest.mark.asyncio
async def test_set_success(redis_client, mock_redis_client):
    key = "test_key"
    value = {"a": 1}
    ttl = 60

    await redis_client.set(key, value, ttl)

    mock_redis_client.set.assert_awaited_once_with(
        name=key,
        value=json.dumps(value),
        ex=ttl
    )


@pytest.mark.asyncio
async def test_set_error(redis_client, mock_redis_client):
    mock_redis_client.set.side_effect = Exception("redis down")

    with pytest.raises(Exception) as exc:
        await redis_client.set("key", {"x": 1})

    assert "Redis Set error key=key" in str(exc.value)


@pytest.mark.asyncio
async def test_get_success(redis_client, mock_redis_client):
    data = {"hello": "world"}
    mock_redis_client.get.return_value = json.dumps(data)

    result = await redis_client.get("my_key")

    assert result == data
    mock_redis_client.get.assert_awaited_once_with("my_key")


@pytest.mark.asyncio
async def test_get_not_found(redis_client, mock_redis_client):
    mock_redis_client.get.return_value = None

    result = await redis_client.get("missing_key")

    assert result is None


@pytest.mark.asyncio
async def test_get_error(redis_client, mock_redis_client):
    mock_redis_client.get.side_effect = Exception("boom")

    with pytest.raises(Exception) as exc:
        await redis_client.get("key")

    assert "Redis Get error key=key" in str(exc.value)


@pytest.mark.asyncio
async def test_delete_success(redis_client, mock_redis_client):
    mock_redis_client.delete.return_value = 1

    result = await redis_client.delete("key")

    assert result == 1
    mock_redis_client.delete.assert_awaited_once_with("key")


@pytest.mark.asyncio
async def test_delete_error(redis_client, mock_redis_client):
    mock_redis_client.delete.side_effect = Exception("fail")

    with pytest.raises(Exception):
        await redis_client.delete("key")


@pytest.mark.asyncio
async def test_exists_true(redis_client, mock_redis_client):
    mock_redis_client.exists.return_value = 1

    result = await redis_client.exists("key")
    assert result is True


@pytest.mark.asyncio
async def test_exists_false(redis_client, mock_redis_client):
    mock_redis_client.exists.return_value = 0

    result = await redis_client.exists("key")
    assert result is False


@pytest.mark.asyncio
async def test_update_success(redis_client, mock_redis_client):
    key = "key"
    value = {"x": 1}
    ttl = 10

    await redis_client.update(key, value, ttl)

    mock_redis_client.set.assert_awaited_once_with(
        name=key,
        value=json.dumps(value),
        ex=ttl
    )


@pytest.mark.asyncio
async def test_close_success(redis_client, mock_redis_client):
    await redis_client.close()

    mock_redis_client.close.assert_awaited_once()