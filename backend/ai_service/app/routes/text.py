from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from app.services.text_service import TextService
from functools import lru_cache

router = APIRouter(prefix="/v1/text", tags=["Text AI"])

class TextRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    text: str = Field(..., min_length=1, max_length=10_000)


@lru_cache
def get_text_service() -> TextService:
    return TextService()


@router.post("/text_correction", status_code=status.HTTP_200_OK)
async def text_correction(
    request: TextRequest, 
    service: TextService = Depends(get_text_service)):

    try:
        result = await service.text_correction(request.text)
        return {"result": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI processing failed")
    
@router.post("/text_summarization", status_code=status.HTTP_200_OK)
async def text_summarization(
    request: TextRequest,
    service: TextService = Depends(get_text_service)):
    
    try:
        result = await service.text_summarization(request.text)
        return {"result": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")
    

@router.post("/hello", status_code=status.HTTP_200_OK)
async def hello():
    try:
        return {"result": "all alright"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")