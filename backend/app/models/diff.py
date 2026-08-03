"""
Diff Pydantic modelleri — karsilastirma istek/yanit semalari.
"""

from pydantic import BaseModel, Field


# ---------- Request Modelleri ----------

class DiffRequest(BaseModel):
    """POST /prompts/{id}/diff istegi icin body semasi."""
    version_a: int = Field(..., description="Karsilastirilacak ilk versiyon numarasi")
    version_b: int = Field(..., description="Karsilastirilacak ikinci versiyon numarasi")


# ---------- Response Modelleri ----------

class DiffLine(BaseModel):
    """Diff sonucundaki tek bir satir."""
    type: str  # "unchanged", "added", "removed"
    text: str

class DiffResponse(BaseModel):
    """Diff sonucu yanit semasi."""
    version_a: int
    version_b: int
    diff: list[DiffLine]
