from fastapi import APIRouter ,status , Response , HTTPException , Request
from uuid import uuid4
from ..client.redis_client import RedisClient
import time
router = APIRouter(prefix="/v1/session", tags=["Session"])
redis_client = RedisClient()

def generate_uuid():
    return str(uuid4())

def generate_cookie(response: Response, session_id: str):
    response.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/"
    )


@router.post("/session_create", status_code=status.HTTP_201_CREATED)
async def create_session(response: Response):
    session_id = (generate_uuid())
    created_at = int(time.time())
    generate_cookie(response, session_id)
    await redis_client.set(
        key=session_id,
        value={"created_at": created_at},
        ttl=30*24*3600,
    )
    return {"status":"created","session_id": session_id}



@router.post("/session_refresh", status_code=status.HTTP_200_CREATED)
async def session_refresh(request: Request):
    session_id = request.cookies.get("session")
    if session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail="No session cookie")
    await redis_client.expire(
        key =session_id ,
        ttl=30*24*3600,
    )
    return {"status":"refreshed"}

@router.post("/session_validate", status_code=status.HTTP_200_ACCEPTED)
async def session_validate(request: Request):
    session_id = request.cookies.get("session")
    if session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No session cookie")
    exists = await redis_client.exists(session_id)
    if not exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid session cookie")
    return {"status":"valid"}


