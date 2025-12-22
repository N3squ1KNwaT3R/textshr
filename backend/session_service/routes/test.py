import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch, MagicMock

# ⚠️ ВАЖЛИВО: Мокаємо RedisClient ДО імпорту роутера
with patch('session_service.client.redis_client.RedisClient') as MockRedisClient:
    mock_instance = MagicMock()
    mock_instance.set = AsyncMock(return_value=True)
    mock_instance.exists = AsyncMock(return_value=True)
    mock_instance.expire = AsyncMock(return_value=True)
    MockRedisClient.return_value = mock_instance

    # Тепер імпортуємо роутер
    from .session import router

# Створення тестового app
app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestSessionCreate:
    """Тести створення сесії"""

    @patch('session_service.routes.session.redis_client')
    def test_create_session_success(self, mock_redis):
        """Перевірка успішного створення сесії"""
        mock_redis.set = AsyncMock(return_value=True)

        response = client.post("/v1/session/session_create")

        assert response.status_code == 201
        assert response.json()["status"] == "created"
        assert "session_id" in response.json()
        assert "session" in response.cookies


class TestSessionRefresh:
    """Тести оновлення сесії"""

    @patch('session_service.routes.session.redis_client')
    def test_refresh_with_valid_cookie(self, mock_redis):
        """Оновлення з валідним cookie"""
        mock_redis.expire = AsyncMock(return_value=True)

        response = client.post(
            "/v1/session/session_refresh",
            cookies={"session": "test-session-123"}
        )

        assert response.status_code == 200
        assert response.json() == {"status": "refreshed"}

    def test_refresh_without_cookie(self):
        """Оновлення без cookie"""
        response = client.post("/v1/session/session_refresh")

        assert response.status_code == 401
        assert "No session cookie" in response.json()["detail"]


class TestSessionValidate:
    """Тести валідації сесії"""

    @patch('session_service.routes.session.redis_client')
    def test_validate_existing_session(self, mock_redis):
        """Валідація існуючої сесії"""
        mock_redis.exists = AsyncMock(return_value=True)

        response = client.post(
            "/v1/session/session_validate",
            cookies={"session": "valid-session"}
        )

        assert response.status_code == 200
        assert response.json() == {"status": "valid"}

    @patch('session_service.routes.session.redis_client')
    def test_validate_non_existing_session(self, mock_redis):
        """Валідація неіснуючої сесії"""
        mock_redis.exists = AsyncMock(return_value=False)

        response = client.post(
            "/v1/session/session_validate",
            cookies={"session": "invalid-session"}
        )

        assert response.status_code == 401
        assert "Invalid session cookie" in response.json()["detail"]

    def test_validate_without_cookie(self):
        """Валідація без cookie"""
        response = client.post("/v1/session/session_validate")

        assert response.status_code == 401
        assert "No session cookie" in response.json()["detail"]