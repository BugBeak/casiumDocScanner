# backend/schemas.py

from pydantic import BaseModel
from typing import Any, Dict, Optional

class ExtractionCreate(BaseModel):
    document_type: str
    document_content: Dict[str, Any]

class ExtractionResponse(BaseModel):
    id: int
    document_type: str
    document_content: Dict[str, Any]

    class Config:
        orm_mode = True
