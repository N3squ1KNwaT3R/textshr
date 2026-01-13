from fastapi import FastAPI
from .routes.endpoints import router as session_router

app = FastAPI(title="Session Service")
app.include_router(session_router)

@app.get("/")
def read_root():
    return {"session_service": "active"}