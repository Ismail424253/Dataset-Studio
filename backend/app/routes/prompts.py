"""
Prompt route'lari — /prompts endpoint tanimlari.
"""

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models.prompt import PromptCreate, PromptResponse
from app.services import prompt_service

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post(
    "",
    response_model=PromptResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni prompt olustur",
    description="Bir baslik ile yeni bir prompt olusturur.",
)
def create_prompt(body: PromptCreate, conn: sqlite3.Connection = Depends(get_db)):
    """Yeni bir prompt olusturur ve olusturulan kaydi dondurur."""
    prompt = prompt_service.create_prompt(conn, body.title)
    return prompt


@router.get(
    "",
    response_model=list[PromptResponse],
    summary="Tum prompt'lari listele",
    description="Veritabanindaki tum prompt'lari en yeniden eskiye dogru listeler.",
)
def list_prompts(conn: sqlite3.Connection = Depends(get_db)):
    """Tum prompt'lari listeler."""
    return prompt_service.get_all_prompts(conn)
