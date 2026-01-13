from service_typ import session_logic

from fastapi import APIRouter, status, Response, HTTPException, Request
from utils.utils import generate_cookie, get_session
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/session", tags=["Session"])


@router.post("/session_create", status_code=status.HTTP_201_CREATED)
async def create_session(response: Response):
    try:
        session_id = await session_logic.create_session()
        generate_cookie(response, session_id)
        return {"status": "created", "session_id": session_id}
    except session_logic.SessionError as e:
        logger.error(f"create session error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create session")


@router.post("/session_refresh", status_code=status.HTTP_200_OK)
async def session_refresh(request: Request, response: Response):
    try:
        old_session_id = get_session(request)
        new_session_id = await session_logic.refresh_session_logic(old_session_id)
        generate_cookie(response, new_session_id)
        return {"status": "refreshed", "session_id": new_session_id}
    except session_logic.SessionNotFound as e:
        logger.error(f"session_refresh error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No session cookie")
    except session_logic.SessionError as e:
        logger.error(f"session_refresh error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to refresh session")


@router.post("/session_validate", status_code=status.HTTP_200_OK)
async def session_validate(request: Request):
    try:
        session_id = request.cookies.get("session")
        await session_logic.validate_session_logic(session_id)
        return {"status": "valid"}
    except session_logic.SessionNotFound as e:
        logger.error(f"Validate session endpoint failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate session")
    except session_logic.SessionError as e:
        logger.error(f"Validate session endpoint failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to validate session")