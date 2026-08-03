"""
Prompt Versiyon Pydantic modelleri.
"""

from pydantic import BaseModel, Field

# ---------- Request Modelleri ----------

class VersionCreate(BaseModel):
    """POST /prompts/{id}/versions istegi icin body semasi."""
    content: str = Field(..., min_length=1, description="Versiyon icerigi (zorunlu)")

# ---------- Response Modelleri ----------

class VersionResponse(BaseModel):
    """Tek bir versiyonun yanit semasi."""
    id: int
    prompt_id: int
    version_no: int
    content: str
    created_at: str
