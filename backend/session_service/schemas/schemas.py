from pydantic import BaseModel
class SessionCreateResponse(BaseModel):
    status: str
    session_id: str
class SessionRefreshResponse(BaseModel):
    status: str
class SessionValidateResponse(BaseModel):
    status: str