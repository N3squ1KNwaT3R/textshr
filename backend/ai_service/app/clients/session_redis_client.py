import redis.asyncio as redis
import logging
from app.config import redis_settings
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
        """Проверяет существование сессии в Redis"""
        try:
            exists = await self.client.exists(session_id)
            logger.info(f"Session exists check: {session_id} -> {bool(exists)}")
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
        """Закрывает соединение с Redis"""
        try:
            await self.client.close()
            logger.info("SessionRedisClient connection closed")
        except Exception as e:
            logger.error(f"SessionRedisClient close error: {e}")



session_redis_client = SessionRedisClient()