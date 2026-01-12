from schemas.text import (
    TextCreateRequest,
    TextCreateResponse,
    TextGetResponse,
    PasswordRequiredResponse,
    TextUpdateRequest
)
from utils.utils import generate_key, hash_password, verify_password
from config import app_settings

from fastapi.concurrency import run_in_threadpool


class StorageService:

    def __init__(self, redis_service, minio_service):
        self.redis_service = redis_service
        self.minio_service = minio_service

    async def create_text(self, data: TextCreateRequest, creator: str) -> TextCreateResponse:

        while True:
            key = generate_key(data.ttl)
            exists = await self.redis_service.get_from_redis(key)
            if not exists:
                break

        text_size = len(data.text.encode('utf-8'))

        hashed_password = hash_password(data.password) if data.password else None

        if text_size < app_settings.SIZE_THRESHOLD:
            await self.redis_service.save_small_text(
                key=key,
                data=data,
                creator=creator,
                size=text_size,
                password=hashed_password
            )
        else:
            await self.minio_service.save_large_text(
                key=key,
                data=data,
                creator=creator,
                size=text_size,
                password=hashed_password
            )

        return TextCreateResponse(key=key)

    async def _build_text_response(self, key: str, redis_data: dict) -> TextGetResponse:

        if 'link_text' in redis_data:
            text_bytes = await run_in_threadpool(self.minio_service.get_from_minio, key)
            text = text_bytes.decode('utf-8')
        else:
            text = redis_data['text']

        if redis_data.get('only_one_read'):
            await self._delete_text_data(key, redis_data)

        return TextGetResponse(
            text=text,
            size=redis_data['size'],
            summary=redis_data.get('summary')
        )

    async def get_text(self, key: str) -> TextGetResponse | PasswordRequiredResponse | None:
        redis_data = await self.redis_service.get_from_redis(key)
        if not redis_data:
            return None

        if redis_data.get('password'):
            return PasswordRequiredResponse(password_required=True)

        return await self._build_text_response(key, redis_data)

    async def verify_text_password(self, key: str, password: str) -> TextGetResponse | None:
        redis_data = await self.redis_service.get_from_redis(key)
        if not redis_data:
            return None

        if not redis_data.get('password'):
            return None

        if not verify_password(password, redis_data['password']):
            return None

        return await self._build_text_response(key, redis_data)

    async def update_text(self, key: str, data: TextUpdateRequest, creator: str) -> bool:
        old_data = await self.redis_service.get_from_redis(key)
        if not old_data:
            return False

        if old_data['creator'] != creator:
            return False

        await self._delete_text_data(key, old_data)

        text_size = len(data.text.encode("utf-8"))
        hashed_password = hash_password(data.password) if data.password else None

        if text_size < app_settings.SIZE_THRESHOLD:
            await self.redis_service.save_small_text(
                key=key,
                data=data,
                creator=creator,
                size=text_size,
                password=hashed_password
            )
        else:
            await self.minio_service.save_large_text(
                key=key,
                data=data,
                creator=creator,
                size=text_size,
                password=hashed_password
            )

        return True

    async def delete_text(self, key: str, creator: str) -> bool:

        redis_data = await self.redis_service.get_from_redis(key)

        if not redis_data:
            return False

        if redis_data['creator'] != creator:
            return False

        await self._delete_text_data(key, redis_data)

        return True

    async def _delete_text_data(self, key: str, redis_data: dict) -> None:

        await self.redis_service.delete_from_redis(key)

        if 'link_text' in redis_data:
            await run_in_threadpool(self.minio_service.delete_from_minio, key)
