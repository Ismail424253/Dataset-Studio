from pydantic import BaseModel, Field

class TagResponse(BaseModel):
    id: int
    name: str

class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Etiket adi")

class PromptTagAttach(BaseModel):
    tag_name: str = Field(..., min_length=1, description="Eklenecek etiketin adi")
