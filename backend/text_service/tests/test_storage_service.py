import pytest
from unittest.mock import patch, AsyncMock
from schemas.text import PasswordRequiredResponse


class TestCreateText:

    @pytest.mark.asyncio
    async def test_create_small_text(self, storage_service, mock_redis_client, sample_create_request):
        mock_redis_client.get.return_value = None

        with patch("services.storage_service.generate_key", return_value="abc123"), \
             patch("services.storage_service.hash_password", return_value="hashed_secret"):

            result = await storage_service.create_text(
                sample_create_request, creator="user_1"
            )

        assert result.key == "abc123"
        mock_redis_client.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_large_text(self, storage_service, minio_service, sample_create_request):
        # Arrange
        sample_create_request.text = "x" * 15000  # > SIZE_THRESHOLD

        minio_service.save_large_text = AsyncMock()

        with patch("services.storage_service.generate_key", return_value="large123"), \
                patch("services.storage_service.hash_password", return_value="hashed_secret"):
            # Act
            result = await storage_service.create_text(
                sample_create_request, creator="user_1"
            )

        # Assert
        assert result.key == "large123"
        minio_service.save_large_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_retries_on_collision(self, storage_service, mock_redis_client, sample_create_request):
        mock_redis_client.get.side_effect = [{"exists": True}, None]

        with patch("services.storage_service.generate_key", side_effect=["used", "free"]), \
             patch("services.storage_service.hash_password", return_value="hashed_secret"):

            result = await storage_service.create_text(
                sample_create_request, creator="user_1"
            )

        assert result.key == "free"
        assert mock_redis_client.get.call_count == 2


class TestGetText:

    @pytest.mark.asyncio
    async def test_get_text_success(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "text": "Hello",
            "size": 5,
            "summary": "Test",
            "only_one_read": False
        }

        result = await storage_service.get_text("abc")

        assert result.text == "Hello"
        assert result.size == 5
        assert result.summary == "Test"

    @pytest.mark.asyncio
    async def test_get_text_not_found(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = None

        result = await storage_service.get_text("missing")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_text_requires_password(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "text": "Secret",
            "password": "hashed",
            "size": 6
        }

        result = await storage_service.get_text("abc")

        assert isinstance(result, PasswordRequiredResponse)
        assert result.password_required is True

    @pytest.mark.asyncio
    async def test_get_text_from_minio(self, storage_service, mock_redis_client, mock_minio_client):
        mock_redis_client.get.return_value = {
            "link_text": "minio",
            "size": 15000,
            "only_one_read": False
        }

        mock_minio_client.get.return_value = b"Large text"

        result = await storage_service.get_text("key")

        assert result.text == "Large text"
        mock_minio_client.get.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_get_text_only_one_read(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "text": "Once",
            "size": 4,
            "only_one_read": True
        }

        result = await storage_service.get_text("abc")

        assert result.text == "Once"
        mock_redis_client.delete.assert_called_once_with("abc")


class TestVerifyPassword:

    @pytest.mark.asyncio
    async def test_verify_correct_password(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "text": "Secret",
            "password": "hashed",
            "size": 6,
            "only_one_read": False
        }

        with patch("services.storage_service.verify_password", return_value=True):
            result = await storage_service.verify_text_password("abc", "ok")

        assert result.text == "Secret"

    @pytest.mark.asyncio
    async def test_verify_wrong_password(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "text": "Secret",
            "password": "hashed"
        }

        with patch("services.storage_service.verify_password", return_value=False):
            result = await storage_service.verify_text_password("abc", "bad")

        assert result is None

    @pytest.mark.asyncio
    async def test_verify_no_password(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "text": "Public",
            "size": 6
        }

        result = await storage_service.verify_text_password("abc", "any")

        assert result is None


class TestUpdateText:

    @pytest.mark.asyncio
    async def test_update_success(self, storage_service, mock_redis_client, sample_update_request):
        mock_redis_client.get.return_value = {
            "text": "Old",
            "creator": "user"
        }

        with patch("services.storage_service.hash_password", return_value="hashed"):
            result = await storage_service.update_text("abc", sample_update_request, "user")

        assert result is True
        mock_redis_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_not_owner(self, storage_service, mock_redis_client, sample_update_request):
        mock_redis_client.get.return_value = {
            "creator": "user1"
        }

        result = await storage_service.update_text("abc", sample_update_request, "user2")

        assert result is False

    @pytest.mark.asyncio
    async def test_update_not_found(self, storage_service, mock_redis_client, sample_update_request):
        mock_redis_client.get.return_value = None

        result = await storage_service.update_text("abc", sample_update_request, "user")

        assert result is False


class TestDeleteText:

    @pytest.mark.asyncio
    async def test_delete_success(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "creator": "user"
        }

        result = await storage_service.delete_text("abc", "user")

        assert result is True
        mock_redis_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_not_owner(self, storage_service, mock_redis_client):
        mock_redis_client.get.return_value = {
            "creator": "user1"
        }

        result = await storage_service.delete_text("abc", "user2")

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_with_minio(self, storage_service, mock_redis_client, mock_minio_client):
        mock_redis_client.get.return_value = {
            "creator": "user",
            "link_text": "minio"
        }

        result = await storage_service.delete_text("abc", "user")

        assert result is True
        mock_minio_client.delete.assert_called_once_with("abc")
