"""
Prompt route'lari — /prompts endpoint tanimlari.
"""

import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models.prompt import PromptCreate, PromptUpdate, PromptResponse
from app.models.version import VersionCreate, VersionResponse
from app.models.diff import DiffRequest, DiffResponse
from app.services import prompt_service, version_service, diff_service

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


# ---------- Diff Route'u ----------

@router.post(
    "/{prompt_id}/diff",
    response_model=DiffResponse,
    summary="Iki versiyon arasindaki farki hesapla",
    description="Belirtilen iki versiyon numarasinin icerigini satir bazli karsilastirir.",
)
def compare_versions(prompt_id: int, body: DiffRequest, conn: sqlite3.Connection = Depends(get_db)):
    """Iki versiyon arasindaki diff'i hesaplar ve dondurur."""
    # Ayni versiyon kontrolu
    if body.version_a == body.version_b:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ayni versiyon kendisiyle karsilastirilamaz"
        )

    # Prompt kontrolu
    prompt = prompt_service.get_prompt_by_id(conn, prompt_id)
    if prompt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt bulunamadi"
        )

    # Versiyon A kontrolu
    ver_a = version_service.get_version(conn, prompt_id, body.version_a)
    if ver_a is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Versiyon {body.version_a} bulunamadi"
        )

    # Versiyon B kontrolu
    ver_b = version_service.get_version(conn, prompt_id, body.version_b)
    if ver_b is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Versiyon {body.version_b} bulunamadi"
        )

    # Diff hesapla
    diff_lines = diff_service.compute_diff(ver_a["content"], ver_b["content"])

    return {
        "version_a": body.version_a,
        "version_b": body.version_b,
        "diff": diff_lines,
    }


# ---------- Tag Route'lari (Prompt'a Ozel) ----------

from app.models.tag import TagResponse, PromptTagAttach
from app.services import tag_service

@router.post(
    "/{prompt_id}/tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Prompt'a etiket ekle",
    description="Prompt'a yeni bir etiket ekler (isim uzerinden). Eger etiket yoksa olusturur."
)
def attach_tag(prompt_id: int, body: PromptTagAttach, conn: sqlite3.Connection = Depends(get_db)):
    tag = tag_service.attach_tag_to_prompt(conn, prompt_id, body.tag_name)
    if tag is None:
        raise HTTPException(status_code=404, detail="Prompt bulunamadi")
    return tag

@router.get(
    "/{prompt_id}/tags",
    response_model=list[TagResponse],
    summary="Prompt'un etiketlerini getir"
)
def list_prompt_tags(prompt_id: int, conn: sqlite3.Connection = Depends(get_db)):
    prompt = prompt_service.get_prompt_by_id(conn, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt bulunamadi")
    return tag_service.get_tags_for_prompt(conn, prompt_id)

@router.delete(
    "/{prompt_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Prompt'tan etiket kaldir"
)
def remove_tag(prompt_id: int, tag_id: int, conn: sqlite3.Connection = Depends(get_db)):
    deleted = tag_service.remove_tag_from_prompt(conn, prompt_id, tag_id)
    if not deleted:
        # Prompt veya tag-baglantisi yok
        # Ancak idempotent tutmak daha iyi olabilir, yine de 404 donebiliriz
        raise HTTPException(status_code=404, detail="Iliski bulunamadi")
    return None
