from pydantic import BaseModel, Field
from typing import Optional


class TextCreateRequest(BaseModel):
    text: str = Field(min_length=1)
    ttl: int = Field(gt=0)
    only_one_read: bool = False
    password: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None


class TextUpdateRequest(BaseModel):
    text: str = Field(min_length=1)
    ttl: int = Field(gt=0)
    only_one_read: bool = False
    password: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None


class PasswordVerifyRequest(BaseModel):
    password: str = Field(min_length=1)


class TextCreateResponse(BaseModel):
    key: str


class PasswordRequiredResponse(BaseModel):
    password_required: bool = True


class TextGetResponse(BaseModel):
    text: str
    size: int
    summary: Optional[str] = None


# Redis shemas

class RedisTextSmall(BaseModel):
    text: str
    creator: str
    size: int
    only_one_read: bool
    password: Optional[str] = None
    summary: Optional[str] = None


class RedisTextLarge(BaseModel):
    link_text: str
    creator: str
    size: int
    only_one_read: bool
    password: Optional[str] = None
    summary: Optional[str] = None
    expiresAt: int  # timestamp + ttl
