from pydantic import BaseModel
from typing import Optional
class TextBase(BaseModel):
    link_text: str
    creator: str


class TextSmall(BaseModel):
    text: str
    creator: str
    size: int
    onlyoneread: bool
    password: Optional[str] = None
    summary: Optional[str] = None


class TextLarge(BaseModel):
    link_text: str
    creator: str
    size: int
    onlyoneread: bool
    password: Optional[str] = None
    summary: Optional[str] = None
    expiresAt: int    # timestamp + ttl

class TestModel(BaseModel):
    name: str
    age: int
