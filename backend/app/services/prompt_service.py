"""
Prompt servisi — veritabani islemlerini iceren is mantigi katmani.
"""

import sqlite3
from typing import Optional


def create_prompt(conn: sqlite3.Connection, title: str) -> dict:
    """
    Yeni bir prompt olusturur.

    Args:
        conn: SQLite baglantisi
        title: Prompt basligi

    Returns:
        Olusturulan prompt'un bilgileri (id, title, created_at, updated_at)
    """
    cursor = conn.execute(
        "INSERT INTO prompts (title) VALUES (?)",
        (title,)
    )
    conn.commit()

    # Olusturulan prompt'u geri oku
    row = conn.execute(
        "SELECT id, title, created_at, updated_at FROM prompts WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    return dict(row)


def get_all_prompts(conn: sqlite3.Connection) -> list[dict]:
    """
    Tum prompt'lari listeler (en yeniler ustte).

    Args:
        conn: SQLite baglantisi

    Returns:
        Prompt listesi
    """
    rows = conn.execute(
        "SELECT id, title, created_at, updated_at FROM prompts ORDER BY created_at DESC"
    ).fetchall()

    return [dict(row) for row in rows]


def get_prompt_by_id(conn: sqlite3.Connection, prompt_id: int) -> Optional[dict]:
    """
    Belirtilen id'ye sahip prompt'u getirir.

    Args:
        conn: SQLite baglantisi
        prompt_id: Prompt id

    Returns:
        Prompt bilgileri veya None (bulunamazsa)
    """
    row = conn.execute(
        "SELECT id, title, created_at, updated_at FROM prompts WHERE id = ?",
        (prompt_id,)
    ).fetchone()

    return dict(row) if row else None


def update_prompt(conn: sqlite3.Connection, prompt_id: int, title: str) -> Optional[dict]:
    """
    Belirtilen prompt'un basligini gunceller ve updated_at'i simdi yapar.

    Args:
        conn: SQLite baglantisi
        prompt_id: Prompt id
        title: Yeni baslik

    Returns:
        Guncellenmis prompt bilgileri veya None (bulunamazsa)
    """
    # Prompt'un var olup olmadigini kontrol et
    existing = get_prompt_by_id(conn, prompt_id)
    if existing is None:
        return None

    conn.execute(
        "UPDATE prompts SET title = ?, updated_at = datetime('now') WHERE id = ?",
        (title, prompt_id)
    )
    conn.commit()

    return get_prompt_by_id(conn, prompt_id)


def delete_prompt(conn: sqlite3.Connection, prompt_id: int) -> bool:
    """
    Belirtilen prompt'u siler.
    ON DELETE CASCADE sayesinde iliskili prompt_versions ve prompt_tags
    satirlari otomatik olarak temizlenir.

    Args:
        conn: SQLite baglantisi
        prompt_id: Prompt id

    Returns:
        True (silindi) veya False (bulunamadi)
    """
    cursor = conn.execute(
        "DELETE FROM prompts WHERE id = ?",
        (prompt_id,)
    )
    conn.commit()

    return cursor.rowcount > 0
