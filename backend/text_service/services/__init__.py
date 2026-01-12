from text_service.clients.redis_client import redis_client
from text_service.clients.minio_client import minio_client

from text_service.services.redis_service import RedisService
from text_service.services.minio_service import MinioService
from text_service.services.storage_service import StorageService


redis_service = RedisService(redis_client=redis_client)

minio_service = MinioService(
    minio_client=minio_client,
    redis_client=redis_client
)

storage_service = StorageService(
    redis_service=redis_service,
    minio_service=minio_service
)

__all__ = ["storage_service"]


redis_service = RedisService(redis_client=redis_client)

minio_service = MinioService(
    minio_client=minio_client,
    redis_client=redis_client
)

storage_service = StorageService(
    redis_service=redis_service,
    minio_service=minio_service
)

__all__ = ["storage_service"]