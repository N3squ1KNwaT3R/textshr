from fastapi import FastAPI
from crud.text_crud import router_text
from middleware.cookie_middleware import SessionMiddleware
from clients.redis_client import redis_client
from clients.session_redis_client import session_redis_client
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Text Service", version="1.0.0")

# Підключаємо роутер з префіксом
app.include_router(router_text, prefix="/text", tags=["text"])

# Підключаємо SessionMiddleware з публічними методами
app.add_middleware(
    SessionMiddleware,
    session_redis=session_redis_client,
    exclude_paths=["/docs", "/openapi.json", "/redoc", "/health"],
    public_methods={
        "/text/": ["GET"],        # GET /text/?key=xxx без cookie
        "/text/verify": ["POST"]  # POST /text/verify без cookie (якщо потрібно)
    }
)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    await redis_client.close()
    await session_redis_client.close()
    logger.info("All connections closed")