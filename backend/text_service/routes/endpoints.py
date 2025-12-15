from fastapi import HTTPException, status
from routes.router_create import router
from schemas.text import (
    TextCreateRequest,
    TextCreateResponse,
    TextGetResponse,
    PasswordRequiredResponse,
    PasswordVerifyRequest,
    TextUpdateRequest
)

@router.post("/", response_model=TextCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_text(data: TextCreateRequest):

    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.get("/", response_model=TextGetResponse | PasswordRequiredResponse)
async def get_text(key: str):


    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/verify", response_model=TextGetResponse)
async def verify_text_password(
        data: PasswordVerifyRequest,
        key: str
):


    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_text(
        data: TextUpdateRequest,
        key: str
):


    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_text(key: str):


    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")

