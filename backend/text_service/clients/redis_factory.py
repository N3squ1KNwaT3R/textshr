import redis.asyncio as redis
from config import redis_settings


def create_redis_client():
    return redis.Redis(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        db=redis_settings.REDIS_DB,
        password=redis_settings.REDIS_PASSWORD,
        decode_responses=True
    )
