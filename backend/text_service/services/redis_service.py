from schemas.text import RedisTextSmall, TextCreateRequest


class RedisService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def save_small_text(
            self,
            key: str,
            data: TextCreateRequest,
            creator: str,
            size: int,
            password: str | None
    ) -> None:
        redis_data = RedisTextSmall(
            text=data.text,
            creator=creator,
            size=size,
            only_one_read=data.only_one_read,
            password=password,
            summary=data.summary
        )
        await self.redis_client.set(key, redis_data.model_dump(), ttl=data.ttl)

    async def get_from_redis(self, key: str) -> dict | None:
        return await self.redis_client.get(key)

    async def delete_from_redis(self, key: str) -> None:
        await self.redis_client.delete(key)