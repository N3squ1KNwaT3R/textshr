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
async def text_correction(
    request: TextRequest, 
    service: TextService = Depends(get_text_service)):

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")
    if len(request.text) > 10_000:
        raise HTTPException(status_code=400, detail="Text too long (max 10k chars)")
    
    try:
        result = await service.text_correctione(request.text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

@router.post("/text_summarization", status_code=status.HTTP_200_OK)
async def text_summarization(
    request: TextRequest,
    service: TextService = Depends(get_text_service)):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")
    if len(request.text) > 10_000:
        raise HTTPException(status_code=400, detail="Text too long (max 10k chars)")
    
    try:
        result = await service.text_summarization(request.text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")
    
    

@router.post("/hello", status_code=status.HTTP_200_OK)
async def hello():
    try:
        return {"result": "all alright"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI processing failed")