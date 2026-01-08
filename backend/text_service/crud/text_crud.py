from fastapi import APIRouter, HTTPException, status
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
async def create_text(data: TextCreateRequest):
    creator = "mock_user_cookie"
    return await storage_service.create_text(data, creator)


@router_text.get("/", response_model=TextGetResponse | PasswordRequiredResponse)
async def get_text(key: str):
    result = await storage_service.get_text(key)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Text not found")
    return result


@router_text.post("/verify", response_model=TextGetResponse)
async def verify_text_password(data: PasswordVerifyRequest, key: str):
    result = await storage_service.verify_text_password(key, data.password)
    if result is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password or text not found")
    return result


@router_text.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_text(data: TextUpdateRequest, key: str):
    creator = "mock_user_cookie"
    success = await storage_service.update_text(key, data, creator)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Text not found or access denied")


@router_text.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_text(key: str):
    creator = "mock_user_cookie"
    success = await storage_service.delete_text(key, creator)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Text not found or access denied")
