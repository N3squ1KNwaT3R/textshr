import logging
from uuid import uuid4
from client.redis_client import redis_client
from fastapi import HTTPException, Response, Request

logger = logging.getLogger(__name__)


class Authentication:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.session_ttl = 60 * 60 * 24
        logger.info(f"Authentication initialized with TTL: {self.session_ttl}")

    async def set_cookie(self, response):
        logger.info("=== set_cookie called ===")
        try:
            session_value = self.generate_uuid()
            logger.info(f"Generated session UUID: {session_value}")

            self._generate_cookie(response, session_value)
            logger.info("Cookie generated in response")

            await self.redis.create_session(session_value, ttl=self.session_ttl)
            logger.info(f"✓ Session stored in Redis: {session_value}")

            return response
        except Exception as e:
            logger.error(f"✗ Failed in set_cookie: {e}", exc_info=True)
            raise

    async def refresh_cookie(self, request: Request, response: Response):
        existing_session = request.cookies.get("session", None)

        if not existing_session:
            logger.warning("No session cookie found")
            raise ValueError("No active session found")

        session_exists = await self.redis.exists(existing_session)

        if not session_exists:
            logger.warning(f"Session not found in Redis: {existing_session}")
            raise ValueError("Session expired or invalid")

        await self.redis.refresh_session(existing_session, ttl=self.session_ttl)

    def _generate_cookie(self, response, session_value):
        logger.info(f"Generating cookie with value: {session_value}")
        response.set_cookie(
            key="session",
            value=session_value,
            httponly=True,
            secure=True,
            samesite="strict",
            path="/"
        )

    @staticmethod
    def generate_uuid():
        return str(uuid4())


auth = Authentication(redis_client)
