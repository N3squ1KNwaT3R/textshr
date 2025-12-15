from fastapi import FastAPI
from routes.endpoints import router as text_router

app = FastAPI()

app.include_router(text_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}