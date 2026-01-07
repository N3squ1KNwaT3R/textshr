from uuid import uuid4
from fastapi import Response , HTTPException , Request , status

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


def get_session(request: Request) -> str:
    session_id = request.cookies.get("session")
    if not  session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No session cookie")
    return session_id
