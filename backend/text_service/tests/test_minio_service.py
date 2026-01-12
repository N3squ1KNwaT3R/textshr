import pytest
from unittest.mock import patch
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
async def test_save_large_text(
    minio_service,
    mock_minio_client,
    mock_redis_client,
    sample_text_data
):
    """Тест збереження великого тексту в MinIO"""
    # Arrange
    key = "large123"
    creator = "user_001"
    size = 15000
    password = "hashed_password"

    with patch("time.time", return_value=1_000_000):
        # Act
        await minio_service.save_large_text(
            key=key,
            data=sample_text_data,
            creator=creator,
            size=size,
            password=password
        )

    # ===== MinIO =====
    mock_minio_client.set.assert_called_once()
    minio_args = mock_minio_client.set.call_args.args
    assert minio_args[0] == key
    assert minio_args[1] == b"Hello World"

    # ===== Redis =====
    mock_redis_client.set.assert_called_once()
    redis_args = mock_redis_client.set.call_args.args
    redis_kwargs = mock_redis_client.set.call_args.kwargs

    saved_data = redis_args[1]

    assert saved_data["link_text"] == f"http://minio:9000/{mock_minio_client.bucket}/{key}"
    assert saved_data["creator"] == creator
    assert saved_data["size"] == size
    assert saved_data["expiresAt"] == 1_000_000 + 3600
    assert redis_kwargs["ttl"] == 3600


def test_get_from_minio(minio_service, mock_minio_client):
    """Тест отримання тексту з MinIO"""
    # Arrange
    key = "large123"
    expected_bytes = b"Large text content"
    mock_minio_client.get.return_value = expected_bytes

    # Act
    result = minio_service.get_from_minio(key)

    # Assert
    assert result == expected_bytes
    mock_minio_client.get.assert_called_once_with(key)


def test_delete_from_minio(minio_service, mock_minio_client):
    """Тест видалення з MinIO"""
    # Arrange
    key = "large123"

    # Act
    result = minio_service.delete_from_minio(key)

    # Assert
    assert result is True
    mock_minio_client.delete.assert_called_once_with(key)
