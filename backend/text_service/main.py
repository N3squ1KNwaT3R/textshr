from fastapi import FastAPI
from crud.text_crud import router_text as text_router

app = FastAPI()

app.include_router(text_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}