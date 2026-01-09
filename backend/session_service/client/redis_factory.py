import redis.asyncio as redis
from ..config import get_redis_settings

def create_redis_client():
    settings = get_redis_settings()
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
        decode_responses=True

    )
