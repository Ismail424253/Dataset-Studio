"""
Prompt Pydantic modelleri — istek/yanit sema tanimlari.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------- Request Modelleri ----------

class PromptCreate(BaseModel):
    """POST /prompts istegi icin body semasi."""
    title: str = Field(..., min_length=1, max_length=255, description="Prompt basligi (zorunlu)")


# ---------- Response Modelleri ----------

class PromptResponse(BaseModel):
    """Tek bir prompt'un yanit semasi."""
    id: int
    title: str
    created_at: str
    updated_at: str
