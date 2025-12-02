import json
import logging
from typing import Optional
from redis.exceptions import RedisError

from .redis_factory import create_redis_client

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.redis = create_redis_client()


    async def set(self, key: str, value: dict):
        data = json.dumps(value)
        try:
            result = await self.redis.set(name=key, value=data)
            logger.info(f"SET key={key} success={result}")
            return result
        except RedisError as e:
            logger.error(f"Redis SET error key={key}: {e}")
            raise


    async def get(self, key: str) -> Optional[dict]:
        try:
            data = await self.redis.get(key)
            logger.info(f"GET key={key} found={data is not None}")

            if data is None:
                return None
            return json.loads(data)

        except RedisError as e:
            logger.error(f"Redis GET error key={key}: {e}")
            raise


    async def delete(self, key: str):
        try:
            result = await self.redis.delete(key)
            logger.info(f"DELETE key={key} deleted={result == 1}")
            return result

        except RedisError as e:
            logger.error(f"Redis DELETE error key={key}: {e}")
            raise


    async def exists(self, key: str) -> bool:
        try:
            exists = await self.redis.exists(key)
            exists = exists == 1
            logger.info(f"EXISTS key={key} exists={exists}")
            return exists

        except RedisError as e:
            logger.error(f"Redis EXISTS error key={key}: {e}")
            raise


    async def ping(self) -> bool:
        try:
            response = await self.redis.ping()
            success = response is True
            logger.info(f"PING success={success}")
            return success

        except RedisError as e:
            logger.error(f"Redis PING failed: {e}")
            return False

    async def close(self):
        logger.info("Closing Redis connection")
        await self.redis.close()
        await self.redis.connection_pool.disconnect()

