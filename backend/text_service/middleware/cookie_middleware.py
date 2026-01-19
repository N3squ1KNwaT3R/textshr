# middleware/session_middleware.py
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from clients.session_redis_client import SessionRedisClient

logger = logging.getLogger(__name__)


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, session_redis: SessionRedisClient, exclude_paths: list = None):
        super().__init__(app)
        self.session_redis = session_redis
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/openapi.json",
            "/health",
            "/metrics"
        ]

    async def dispatch(self, request: Request, call_next):
        # Пропускаем исключенные пути
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Получаем session cookie
        session_id = request.cookies.get("session")

        if not session_id:
            logger.warning(f"No session cookie for {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authentication required"}
            )

        # Проверяем сессию
        try:
            exists = await self.session_redis.exists(session_id)

            if not exists:
                logger.warning(f"Invalid session: {session_id}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Session expired or invalid"}
                )

            # Сохраняем session_id для использования в эндпоинтах
            request.state.session_id = session_id
            logger.info(f"Valid session: {session_id} for path: {request.url.path}")

            response = await call_next(request)
            return response

        except Exception as e:
            logger.error(f"Session validation error: {e}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": "Session service unavailable"}
            )