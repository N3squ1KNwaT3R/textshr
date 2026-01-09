from pydantic import BaseModel
class BaseResponse(BaseModel):
    status: str
class SessionCreateResponse(BaseResponse):
    session_id: str
class SessionRefreshResponse(BaseResponse):
    pass
class SessionValidateResponse(BaseResponse):
    pass



