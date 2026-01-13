'''import pytest
from unittest.mock import MagicMock, patch
from ..clients.minio_client import MinioClient


@pytest.fixture
def mock_minio():
    """Створюємо моканий Minio client."""
    return MagicMock()


@pytest.fixture
def minio_client(mock_minio):
    """Підміняємо create_minio_client() щоб MinioClient використовував mock."""
    with patch("text_service.clients.minio_client.create_minio_client", return_value=mock_minio):
        client = MinioClient()
        client.client = mock_minio  # про всяк випадок
        return client


def test_set(minio_client, mock_minio):
    minio_client.set("file.txt", b"hello")
    mock_minio.put_object.assert_called_once()


def test_get(minio_client, mock_minio):
    mock_response = MagicMock()
    mock_response.read.return_value = b"content"
    mock_minio.get_object.return_value = mock_response

    data = minio_client.get("file.txt")

    assert data == b"content"
    mock_minio.get_object.assert_called_once()


def test_exists_true(minio_client, mock_minio):
    mock_minio.stat_object.return_value = True
    assert minio_client._exists("file.txt") is True


def test_exists_false(minio_client, mock_minio):
    mock_minio.stat_object.side_effect = Exception("not found")
    assert minio_client._exists("file.txt") is False


def test_delete_true(minio_client, mock_minio):
    mock_minio.stat_object.return_value = True  # exists
    result = minio_client.delete("file.txt")

    assert result is True
    mock_minio.remove_object.assert_called_once()


def test_delete_false(minio_client, mock_minio):
    mock_minio.stat_object.side_effect = Exception("not found")

    result = minio_client.delete("file.txt")
    assert result is False
    mock_minio.remove_object.assert_not_called()


def test_update_true(minio_client, mock_minio):
    mock_minio.stat_object.return_value = True

    result = minio_client.update("file.txt", b"new data")

    assert result is True
    mock_minio.put_object.assert_called_once()


def test_update_false(minio_client, mock_minio):
    mock_minio.stat_object.side_effect = Exception("not found")

    result = minio_client.update("missing.txt", b"new data")

    assert result is False
    mock_minio.put_object.assert_not_called()'''
