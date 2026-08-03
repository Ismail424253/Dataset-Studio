"""
Prompt route'lari — /prompts endpoint tanimlari.
"""

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models.prompt import PromptCreate, PromptUpdate, PromptResponse
from app.models.version import VersionCreate, VersionResponse
from app.services import prompt_service, version_service

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
    prompt = prompt_service.create_prompt(conn, body.title, body.content)
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


@router.get(
    "/{prompt_id}",
    response_model=PromptResponse,
    summary="Prompt detayi getir",
    description="Belirtilen id'ye sahip prompt'u getirir.",
)
def get_prompt(prompt_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Tek bir prompt'u id'ye gore getirir."""
    prompt = prompt_service.get_prompt_by_id(conn, prompt_id)
    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt bulunamadi"
        )
    return prompt


@router.patch(
    "/{prompt_id}",
    response_model=PromptResponse,
    summary="Prompt guncelle",
    description="Belirtilen prompt'un basligini gunceller.",
)
def update_prompt(prompt_id: int, body: PromptUpdate, conn: sqlite3.Connection = Depends(get_db)):
    """Prompt basligini gunceller ve updated_at alanini yeniler."""
    prompt = prompt_service.update_prompt(conn, prompt_id, body.title)
    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt bulunamadi"
        )
    return prompt


@router.delete(
    "/{prompt_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Prompt sil",
    description="Belirtilen prompt'u ve iliskili versiyonlarini/etiketlerini siler.",
)
def delete_prompt(prompt_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Prompt'u siler. CASCADE ile iliskili kayitlar otomatik temizlenir."""
    deleted = prompt_service.delete_prompt(conn, prompt_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt bulunamadi"
        )
    return None


# ---------- Versiyon Route'lari ----------

@router.post(
    "/{prompt_id}/versions",
    response_model=VersionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni versiyon ekle",
    description="Mevcut bir prompt'a yeni bir versiyon ekler ve updated_at'i gunceller.",
)
def add_version(prompt_id: int, body: VersionCreate, conn: sqlite3.Connection = Depends(get_db)):
    """Prompt'a yeni bir versiyon ekler."""
    version = version_service.add_version(conn, prompt_id, body.content)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt bulunamadi"
        )
    return version


@router.get(
    "/{prompt_id}/versions",
    response_model=list[VersionResponse],
    summary="Prompt versiyonlarini listele",
    description="Bir prompt'un tum versiyonlarini artan sirayla getirir.",
)
def list_versions(prompt_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Prompt'un versiyonlarini listeler."""
    prompt = prompt_service.get_prompt_by_id(conn, prompt_id)
    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt bulunamadi"
        )
    return version_service.get_versions(conn, prompt_id)


@router.get(
    "/{prompt_id}/versions/{version_no}",
    response_model=VersionResponse,
    summary="Belirli bir versiyonu getir",
    description="Prompt'un istenen versiyon numarali icerigini getirir.",
)
def get_version(prompt_id: int, version_no: int, conn: sqlite3.Connection = Depends(get_db)):
    """Prompt'un spesifik bir versiyonunu getirir."""
    version = version_service.get_version(conn, prompt_id, version_no)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt veya versiyon bulunamadi"
        )
    return version
