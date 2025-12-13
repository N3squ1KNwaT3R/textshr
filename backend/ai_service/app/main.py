from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import text

app = FastAPI(
    title="AI Service",
    description="AI service for text and image generation",
    version="1.0.0",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text.router)