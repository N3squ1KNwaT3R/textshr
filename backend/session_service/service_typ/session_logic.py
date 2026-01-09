import time
import logging
from session_service.client.redis_client import RedisClient
from ..utils.utils import generate_uuid
from fastapi import Request, HTTPException, status
logger = logging.getLogger(__name__)
redis_client = RedisClient()
SESSION_TTL = 30 * 24 * 3600

class SessionError(Exception):
    pass
class SessionNotFound(SessionError):
    pass
class SessionSaveError(SessionError):
    pass


async def create_session() -> str:
    try:
        session_id = generate_uuid()
        await save_session(session_id)
    except Exception as e:
        logger.error(f"Session create failed  {e}")
        raise SessionError("Session create failed ")
    return session_id


async def refresh_session_logic(old_session_id: str) -> str:
        exists = await redis_client.exists(old_session_id)
        if not exists:
            logger.warning(f"Session refresh failed: session {old_session_id} not found")
            raise SessionNotFound("Old session not found ")
        try:
            new_session_id = generate_uuid()
            await redis_client.delete(old_session_id)
            await save_session(new_session_id)
            logger.info(f"New session id {new_session_id}")
            return new_session_id
        except Exception as e:
            logger.error(f"Session refresh failed  {e}")
            raise SessionError("Session refresh failed ")


async def validate_session_logic(session_id: str) -> None:
        if not session_id:
            raise SessionNotFound("Session not found ")
        exists = await redis_client.exists(session_id)
        if not exists:
            raise SessionNotFound("Session not found ")



async def save_session(session_id: str) -> None:
        try:
            created_at = int(time.time())
            await redis_client.set(
                key=session_id,
                value={"created_at": created_at},
                ttl=SESSION_TTL,
            )
            logger.info(f"Save session id {session_id}")
        except Exception as e:
            logger.error(f"Session save failed  {e}")
            raise SessionSaveError("Session save failed ")

