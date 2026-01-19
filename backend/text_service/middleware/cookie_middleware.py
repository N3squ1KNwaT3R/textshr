import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            session_redis,
            exclude_paths: list = None,
            public_methods: dict = None
    ):
        super().__init__(app)
        self.session_redis = session_redis
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/openapi.json",
            "/redoc",
            "/health",
            "/metrics"
        ]
        # Формат: {"шлях": ["GET", "POST"]}
        self.public_methods = public_methods or {}
        logger.info(f"SessionMiddleware initialized with public_methods: {self.public_methods}")

    def _is_public_request(self, path: str, method: str) -> bool:
        """Перевірка чи запит публічний (не потребує сесії)"""
        for public_path, methods in self.public_methods.items():
            if path.startswith(public_path) and method in methods:
                logger.debug(f"Public request matched: {method} {path}")
                return True
        return False

    def _is_excluded_path(self, path: str) -> bool:
        """Перевірка чи шлях повністю виключено"""
        return any(path.startswith(excluded) for excluded in self.exclude_paths)

    async def dispatch(self, request: Request, call_next):
        # Пропускаємо OPTIONS для CORS
        if request.method == "OPTIONS":
            return await call_next(request)

        # Пропускаємо повністю виключені шляхи
        if self._is_excluded_path(request.url.path):
            return await call_next(request)

        # Перевіряємо чи це публічний запит
        if self._is_public_request(request.url.path, request.method):
            request.state.session_id = None  # Публічний запит без сесії
            logger.info(f"✓ Public request allowed: {request.method} {request.url.path}")
            return await call_next(request)

        # Отримуємо session cookie
        session_id = request.cookies.get("session")

        if not session_id:
            logger.warning(f"✗ No session cookie for {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authentication required"}
            )

        # Перевіряємо сесію
        try:
            exists = await self.session_redis.exists(session_id)

            if not exists:
                logger.warning(f"✗ Invalid session: {session_id}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Session expired or invalid"}
                )

            request.state.session_id = session_id
            logger.info(f"✓ Valid session: {session_id} for path: {request.url.path}")

            response = await call_next(request)
            return response

        except Exception as e:
            logger.error(f"✗ Session validation error: {e}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": "Session service unavailable"}
            )