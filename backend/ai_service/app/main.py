from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routes.text import router
from app.middleware.cookie_middleware import SessionMiddleware
from app.clients.session_redis_client import session_redis_client

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text Service",
    description="Service for storing and retrieving texts",
    version="1.0.0",
    redoc_url=None
)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    SessionMiddleware,
    session_redis=session_redis_client,
    exclude_paths=["/docs", "/openapi.json", "/health"]
)



@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    await session_redis_client.close()
    logger.info("All connections closed")
