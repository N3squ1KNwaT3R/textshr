import redis.asyncio as redis
import logging
from config import redis_settings
logger = logging.getLogger(__name__)


class SessionRedisClient:

    def __init__(self):
        self.client = redis.Redis(
            host=redis_settings.REDIS_HOST,
            port=redis_settings.REDIS_PORT,
            password=redis_settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=5
        )
        logger.info(
            f"SessionRedisClient initialized: "
            f"{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}"
        )

    async def exists(self, session_id: str) -> bool:
        """Перевіряє чи існує сесія в Redis"""
        try:
            # ВАЖЛИВО: Додаємо prefix "session:"
            key = f"session:{session_id}"
            exists = await self.client.exists(key)
            logger.info(f"Session exists check: {key} -> {bool(exists)}")
            return bool(exists)
        except redis.AuthenticationError as e:
            logger.error(f"Redis authentication failed: {e}")
            raise
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            raise
        except Exception as e:
            logger.error(f"Session exists error {session_id}: {e}")
            raise

    async def close(self):
        """Закриває з'єднання з Redis"""
        try:
            await self.client.close()
            logger.info("SessionRedisClient connection closed")
        except Exception as e:
            logger.error(f"SessionRedisClient close error: {e}")


session_redis_client = SessionRedisClient()