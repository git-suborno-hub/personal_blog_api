from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T=TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    code: Optional[str] = None

class MessageResponse(BaseModel):
    success: bool = True
    message: str