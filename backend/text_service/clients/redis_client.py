import logging
from typing import Optional

from clients.redis_factory import create_redis_client

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.redis = create_redis_client()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def set(self, key: str, value: dict, ttl: Optional[int] = None):
        mapping = {}
        for k, v in value.items():
            if v is None:
                mapping[k] = ""
            elif isinstance(v, bool):
                mapping[k] = "1" if v else "0"
            else:
                mapping[k] = str(v)
        try:
            await self.redis.hset(name=key, mapping=mapping)
            is_large_text = 'expiresAt' in value
            if is_large_text:
                await self.redis.zadd("notes:expiry", {key: int(value['expiresAt'])})
            else:
                await self.redis.expire(key, ttl)
            logger.info(f"HSET {key} -> {value}")
        except Exception as e:
            raise Exception(f"Redis HSET error key={key}: {e}")

    async def get(self, key: str) -> Optional[dict]:
        try:
            # Отримуємо всі поля з hash
            data = await self.redis.hgetall(key)

            if not data:
                logger.info(f"GET HASH key={key} -> NOT FOUND")
                return None

            # Конвертуємо bytes в strings і парсимо типи
            result = {}
            for k, v in data.items():
                k_str = k.decode('utf-8') if isinstance(k, bytes) else k
                v_str = v.decode('utf-8') if isinstance(v, bytes) else v

                # Boolean поля (only_one_read)
                if k_str == 'only_one_read':
                    result[k_str] = v_str == '1'
                # Integer поля (size, expiresAt)
                elif k_str in ('size', 'expiresAt') and v_str.isdigit():
                    result[k_str] = int(v_str)
                # Пусті значення (None)
                elif v_str == "":
                    result[k_str] = None
                else:
                    result[k_str] = v_str

            logger.info(f"GET HASH key={key} -> Found")
            return result

        except Exception as e:
            raise Exception(f"Redis GET error key={key}: {e}")

    async def update(self, key: str, value: dict, ttl: Optional[int] = None):
        try:
            exists = await self._exists(key)
            if exists:
                await self.redis.zrem("notes:expiry", key)
                await self.redis.delete(key)
                await self.set(key, value, ttl)
                logger.info(f"UPDATE {key} completed")
                return True
            return False
        except Exception as e:
            raise Exception(f"Redis UPDATE error key={key}: {e}")

    async def delete(self, key: str):
        try:
            exists = await self._exists(key)
            if not exists:
                return False

            await self.redis.zrem("notes:expiry", key)

            await self.redis.delete(key)

            logger.info(f"DELETE key={key}")
            return True

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

redis_client = RedisClient()
