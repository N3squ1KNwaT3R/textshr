from app.config import settings
from typing import Dict

class TextService:
    async def text_correction(self, text: str) -> Dict[str, str]:
        return {"text": "Corrected text here"}

    async def text_summarization(self, text: str) -> Dict[str, str]:
        return {"text": "Summarized text here"}