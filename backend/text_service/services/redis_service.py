from schemas.text import RedisTextSmall


class RedisService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def save_small_text(
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
        redis_data = RedisTextSmall(
            text=text,
            creator=creator,
            size=size,
            only_one_read=only_one_read,
            password=password,
            summary=summary
        )
        await self.redis_client.set(key, redis_data.model_dump(), ttl=ttl)

    async def get_from_redis(self, key: str) -> dict | None:
        return await self.redis_client.get(key)

    async def delete_from_redis(self, key: str) -> None:
        await self.redis_client.delete(key)