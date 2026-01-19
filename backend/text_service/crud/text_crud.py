from fastapi import APIRouter, HTTPException, status, Request
from services import storage_service
from schemas.text import (
    TextCreateRequest,
    TextCreateResponse,
    TextGetResponse,
    PasswordRequiredResponse,
    PasswordVerifyRequest,
    TextUpdateRequest
)

router_text = APIRouter()


@router_text.post("/", response_model=TextCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_text(data: TextCreateRequest, request: Request):
    session_id = request.state.session_id
    return await storage_service.create_text(data, session_id)


@router_text.get("/", response_model=TextGetResponse | PasswordRequiredResponse)
async def get_text(key: str, request: Request):
    result = await storage_service.get_text(key)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text not found"
        )
    return result


@router_text.post("/verify", response_model=TextGetResponse)
async def verify_text_password(data: PasswordVerifyRequest, key: str, request: Request):
    result = await storage_service.verify_text_password(key, data.password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong password or text not found"
        )
    return result


@router_text.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_text(data: TextUpdateRequest, key: str, request: Request):
    session_id = request.state.session_id

    success = await storage_service.update_text(key, data, session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text not found or access denied"
        )
    return {"success": True}


@router_text.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_text(key: str, request: Request):
    session_id = request.state.session_id

    success = await storage_service.delete_text(key, session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text not found or access denied"
        )
    return {"success": True}
