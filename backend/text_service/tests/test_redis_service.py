import pytest
from schemas.text import TextCreateRequest


# ========= FIXTURES =========

@pytest.fixture
def sample_text_data():
    return TextCreateRequest(
        text="Hello World",
        ttl=3600,
        only_one_read=False,
        password=None,
        summary="Test summary"
    )


# ========= TESTS =========

@pytest.mark.asyncio
async def test_save_small_text(redis_service, mock_redis_client, sample_text_data):
    """Тест збереження малого тексту в Redis"""
    # Arrange
    key = "test123"
    creator = "user_001"
    size = 11
    password = "hashed_password"

    # Act
    await redis_service.save_small_text(
        key=key,
        data=sample_text_data,
        creator=creator,
        size=size,
        password=password
    )

    # Assert
    mock_redis_client.set.assert_called_once()
    call_args = mock_redis_client.set.call_args

    # key
    assert call_args.args[0] == key

    # ttl
    assert call_args.kwargs["ttl"] == 3600

    # data
    saved_data = call_args.args[1]
    assert saved_data["text"] == "Hello World"
    assert saved_data["creator"] == creator
    assert saved_data["size"] == size
    assert saved_data["password"] == password
    assert saved_data["summary"] == "Test summary"


@pytest.mark.asyncio
async def test_get_from_redis_exists(redis_service, mock_redis_client):
    """Тест отримання існуючого тексту з Redis"""
    # Arrange
    key = "test123"
    expected_data = {
        "text": "Hello",
        "creator": "user_001",
        "size": 5
    }
    mock_redis_client.get.return_value = expected_data

    # Act
    result = await redis_service.get_from_redis(key)

    # Assert
    assert result == expected_data
    mock_redis_client.get.assert_called_once_with(key)


@pytest.mark.asyncio
async def test_get_from_redis_not_exists(redis_service, mock_redis_client):
    """Тест отримання неіснуючого тексту"""
    # Arrange
    mock_redis_client.get.return_value = None

    # Act
    result = await redis_service.get_from_redis("nonexistent")

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_delete_from_redis(redis_service, mock_redis_client):
    """Тест видалення з Redis"""
    # Arrange
    key = "test123"

    # Act
    await redis_service.delete_from_redis(key)

    # Assert
    mock_redis_client.delete.assert_called_once_with(key)
