from fastapi import APIRouter, status, HTTPException, Response
import logging
from api.router import session_router
from services.session_logic import auth
logger = logging.getLogger(__name__)
from fastapi import HTTPException, Response, Request
from fastapi.responses import JSONResponse


@session_router.post("/create")
async def create_session(request: Request):
    response = JSONResponse(content={"status": "success"})
    existing_session = request.cookies.get("session")

    if existing_session:
        logger.warning(f"Session already exists: {existing_session}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session already exists"
        )

    try:
        response = await auth.set_cookie(response)
        return response
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")


@session_router.post("/session_refresh", status_code=status.HTTP_200_OK)
async def session_refresh(request: Request):
    try:
        response = JSONResponse(content={"status": "success"})
        response = await auth.refresh_cookie(request, response)
        return response
    except ValueError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to refresh session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to refresh session")
