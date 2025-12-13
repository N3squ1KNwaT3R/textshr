from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.services.text_service import TextService

router = APIRouter(prefix="/v1/text", tags=["Text AI"])

class TextRequest(BaseModel):
    #Wait to change, it depends on text service
    text: str

def get_text_service():
    return TextService()

@router.post("/text_correction", status_code=status.HTTP_200_OK)
async def text_correction(request: TextRequest) -> dict:
    pass


@router.post("/text_summarization", status_code=status.HTTP_200_OK)
async def text_summarization(request: TextRequest) -> dict:
    pass    