from fastapi import FastAPI
from api.session import session_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Session service")
app.include_router(session_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
