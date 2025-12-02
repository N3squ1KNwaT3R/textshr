import redis.asyncio as aioredis
from ..config import settings

def create_redis_client():
    return aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        ssl=settings.REDIS_TLS or False,
        decode_responses=True
    )
