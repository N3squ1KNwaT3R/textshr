import redis.asyncio as redis
import json
import logging
from typing import Optional
from functools import lru_cache
from .redis_factory import create_redis_client

logger = logging.getLogger(__name__)


@lru_cache()
def get_redis_client() -> redis.Redis:
    return create_redis_client()


class RedisClient:
    def __init__(self, client: redis.Redis = None):
        self.client = client or get_redis_client()

    async def set(self, key: str, value: dict, ttl: Optional[int] = None):
        data = json.dumps(value)
        try:
            await self.client.set(name=key, value=data, ex=ttl)
            logger.info(f"Redis set {key} -> {data}")
        except Exception as e:
            logger.error(f"Redis Set error key={key}: {e}")
            raise Exception(f"Redis Set error key={key}: {e}")

    async def get(self, key: str) -> Optional[dict]:
        try:
            data = await self.client.get(key)
            if not data:
                logger.warning(f"Redis get {key} -> Not found")
                return None
            logger.info(f"Redis get = {key}")
            data = json.loads(data)
            return data
        except Exception as e:
            logger.error(f"Redis GET error key={key}: {e}")
            raise Exception(f"Redis Get error key={key}: {e}")

    async def delete(self, key: str):
        try:
            result = await self.client.delete(key)
            logger.info(f"Redis Delete {key} -> {result}")
            return result
        except Exception as e:
            logger.error(f"Redis Delete error key={key}: {e}")
            raise Exception(f"Redis Delete error key={key}: {e}")

    async def exists(self, key: str) -> bool:
        try:
            exists = await self.client.exists(key)
            logger.info(f"Redis exists {key} -> {exists}")
            return bool(exists)
        except Exception as e:
            logger.error(f"Redis Exists error key={key}: {e}")
            raise Exception(f"Redis Exists error key={key}: {e}")

    async def update(self, key: str, value: dict, ttl: Optional[int] = None):
        await self.set(key, value, ttl)

    async def close(self):
        try:
            await self.client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Redis close error: {e}")

    async def expire(self, key: str, ttl: int) -> bool:
        try:
            result = await self.client.expire(key, ttl)
            logger.info(f"Redis expire {key} -> {ttl}")
            return result
        except Exception as e:
            logger.error(f"Redis expire error: {e}")
            return False