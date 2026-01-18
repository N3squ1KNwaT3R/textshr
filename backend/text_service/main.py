from fastapi import FastAPI
from crud.text_crud import router_text as text_router
from middleware.cookie_middleware import SessionMiddleware
from clients.redis_client import redis_client
from clients.session_redis_client import session_redis_client
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Text Service", version="1.0.0")

app.include_router(text_router)

app.add_middleware(
    SessionMiddleware,
    session_redis=session_redis_client,
    exclude_paths=["/docs", "/openapi.json", "/health"]
)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    await redis_client.close()
    await session_redis_client.close()
    logger.info("All connections closed")
