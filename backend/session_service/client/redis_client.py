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

    async def create_session(self, session_id: str, ttl: Optional[int] = None):
        try:
            await self.client.set(name=session_id, value="active", ex=ttl)
            logger.info(f"Session created: {session_id}")
        except Exception as e:
            logger.error(f"Redis session creation error {session_id}: {e}")
            raise

    async def refresh_session(self, session_id: str, ttl: int):
        logger.info(f"Refreshing session: {session_id} with new TTL: {ttl}")
        try:
            await self.client.expire(session_id, ttl)
            logger.info(f"✓ Session TTL updated: {session_id}")
        except Exception as e:
            logger.error(f"✗ Failed to refresh session {session_id}: {e}", exc_info=True)
            raise

    async def exists(self, key: str) -> bool:
        try:
            exists = await self.client.exists(key)
            logger.info(f"Redis exists {key} -> {exists}")
            return bool(exists)
        except Exception as e:
            logger.error(f"Redis Exists error key={key}: {e}")
            raise Exception(f"Redis Exists error key={key}: {e}")

    async def close(self):
        try:
            await self.client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Redis close error: {e}")

redis_client = RedisClient()