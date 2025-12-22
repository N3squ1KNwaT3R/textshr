import json
import logging
from typing import Optional

from .redis_factory import create_redis_client

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.redis = create_redis_client()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def set(self, key: str, value: dict, ttl: Optional[int] = None):
        data = json.dumps(value)
        try:
            await self.redis.set(name=key, value=data, ex=ttl)
            logger.info(f"SET {key} -> {data}")
        except Exception as e:
            raise Exception(f"Redis SET error key={key}: {e}")

    async def get(self, key: str) -> Optional[dict]:
        try:
            data = await self.redis.get(key)
            if data is None:
                logger.info(f"GET key={key} -> NOT FOUND")
                return None
            logger.info(f"GET key={key}")
            data = json.loads(data)
            return data
        except Exception as e:
            raise Exception(f"Redis GET error key={key}: {e}")

    async def update(self, key: str, value: dict, ttl: Optional[int] = None):
        try:
            exists = await self._exists(key)
            if exists:
                await self.redis.delete(key)
                data = json.dumps(value)
                await self.redis.set(name=key, value=data, ex=ttl)
                logger.info(f"UPDATE {key} -> {data}")
                return True
            return False
        except Exception as e:
            raise Exception(f"Redis UPDATE error key={key}: {e}")

    async def delete(self, key: str):
        try:
            exists = await self._exists(key)
            if exists:
                await self.redis.delete(key)
                logger.info(f"DELETE key={key}")
                return True
            return False

        except Exception as e:
            raise Exception(f"Redis DELETE error key={key}: {e}")

    async def _exists(self, key: str) -> bool:
        try:
            exists = await self.redis.exists(key)
            logger.info(f"EXISTS key={key} exists={exists}")
            return bool(exists)

        except Exception as e:
            raise Exception(f"Redis EXISTS error key={key}: {e}")

    async def ping(self) -> bool:
        try:
            response = await self.redis.ping()
            logger.info(f"PING success={response}")
            return response in (True, "PONG", b"PONG")

        except Exception as e:
            logger.error(f"Redis PING failed: {e}")
            return False

    async def close(self):
        await self.redis.close()
        await self.redis.connection_pool.disconnect()
        logger.info("Close Redis connection")

text_client = RedisClient()
