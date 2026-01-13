"""
Fixtures для тестів
Все mock'ається, реальні Redis/MinIO не використовуються
"""

import pytest
from unittest.mock import AsyncMock, Mock, MagicMock, patch
import sys
from pathlib import Path

# Додаємо шлях
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============= MOCK CLIENTS ПЕРЕД БУДЬ-ЯКИМ ІМПОРТОМ =============

# Mock Redis client
mock_redis_client_global = AsyncMock()
mock_redis_client_global.set = AsyncMock(return_value=True)
mock_redis_client_global.get = AsyncMock(return_value=None)
mock_redis_client_global.delete = AsyncMock(return_value=True)

# Mock MinIO client
mock_minio_client_global = Mock()
mock_minio_client_global.bucket = "test-bucket"
mock_minio_client_global.set = Mock()
mock_minio_client_global.get = Mock(return_value=b"Mock text")
mock_minio_client_global.delete = Mock(return_value=True)

# Patch clients модулі ПЕРЕД імпортом
sys.modules['clients.redis_client'] = MagicMock()
sys.modules['clients.redis_client'].text_client = mock_redis_client_global
sys.modules['clients.redis_client'].redis_client = mock_redis_client_global

sys.modules['clients.minio_client'] = MagicMock()
sys.modules['clients.minio_client'].minio_client = mock_minio_client_global

# Mock config
mock_app_settings = MagicMock()
mock_app_settings.SIZE_THRESHOLD = 10240

config_mock = MagicMock()
config_mock.app_settings = mock_app_settings
sys.modules['config'] = config_mock

# ============= ТЕПЕР МОЖНА ІМПОРТУВАТИ =============

from services.redis_service import RedisService
from services.minio_service import MinioService
from services.storage_service import StorageService
from schemas.text import TextCreateRequest, TextUpdateRequest


# ============= FIXTURES =============

@pytest.fixture
def mock_redis_client():
    """Mock Redis client для кожного тесту"""
    client = AsyncMock()
    client.set = AsyncMock(return_value=True)
    client.get = AsyncMock(return_value=None)
    client.delete = AsyncMock(return_value=True)
    return client


@pytest.fixture
def mock_minio_client():
    """Mock MinIO client для кожного тесту"""
    client = Mock()
    client.bucket = "test-bucket"
    client.set = Mock(return_value=None)
    client.get = Mock(return_value=b"Mock text content")
    client.delete = Mock(return_value=True)
    return client


@pytest.fixture
def redis_service(mock_redis_client):
    """Redis service з mock client"""
    return RedisService(redis_client=mock_redis_client)


@pytest.fixture
def minio_service(mock_minio_client, mock_redis_client):
    """MinIO service з mock clients"""
    return MinioService(
        minio_client=mock_minio_client,
        redis_client=mock_redis_client
    )


@pytest.fixture
def storage_service(redis_service, minio_service):
    """Storage service - головний сервіс"""
    return StorageService(
        redis_service=redis_service,
        minio_service=minio_service
    )


@pytest.fixture
def sample_create_request():
    """Приклад запиту на створення тексту"""
    return TextCreateRequest(
        text="Test text",
        ttl=3600,
        only_one_read=False,
        password="secret",
        summary="Test summary"
    )


@pytest.fixture
def sample_update_request():
    """Приклад запиту на оновлення тексту"""
    return TextUpdateRequest(
        text="Updated text",
        ttl=7200,
        only_one_read=True,
        password="new_secret",
        summary="Updated summary"
    )