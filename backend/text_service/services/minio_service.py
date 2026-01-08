from schemas.text import RedisTextLarge
import time


class MinioService:
    def __init__(self, minio_client, redis_client):
        self.minio_client = minio_client
        self.redis_client = redis_client

    async def save_large_text(
            self,
            key: str,
            text: str,
            creator: str,
            size: int,
            ttl: int,
            only_one_read: bool,
            password: str | None,
            summary: str | None
    ) -> None:
        text_bytes = text.encode('utf-8')
        self.minio_client.set(key, text_bytes)

        link = f"http://minio:9000/{self.minio_client.bucket}/{key}"
        expires_at = int(time.time()) + ttl

        redis_data = RedisTextLarge(
            link_text=link,
            creator=creator,
            size=size,
            only_one_read=only_one_read,
            password=password,
            summary=summary,
            expiresAt=expires_at
        )
        await self.redis_client.set(key, redis_data.model_dump(), ttl=ttl)

    def get_from_minio(self, key: str) -> bytes:
        return self.minio_client.get(key)

    def delete_from_minio(self, key: str) -> bool:
        return self.minio_client.delete(key)