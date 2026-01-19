from schemas.text import RedisTextLarge, TextCreateRequest
import time


class MinioService:
    def __init__(self, minio_client, redis_client):
        self.minio_client = minio_client
        self.redis_client = redis_client

    async def save_large_text(
        self,
        key: str,
        data: TextCreateRequest,
        creator: str,
        size: int,
        password: str | None
    ) -> None:
        text_bytes = data.text.encode("utf-8")
        self.minio_client.set(key, text_bytes)

        link = f"{key}"
        expires_at = float((time.time()) + data.ttl)*1000

        redis_data = RedisTextLarge(
            link_text=link,
            creator=creator,
            size=size,
            only_one_read=data.only_one_read,
            password=password,
            summary=data.summary,
            expiresAt=expires_at
        )

        await self.redis_client.set(
            key,
            redis_data.model_dump()
        )

    def get_from_minio(self, key: str) -> bytes:
        return self.minio_client.get(key)

    def delete_from_minio(self, key: str) -> bool:
        return self.minio_client.delete(key)
