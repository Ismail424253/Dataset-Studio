"""
Prompt servisi — veritabani islemlerini iceren is mantigi katmani.
"""

import sqlite3
from typing import Optional


def create_prompt(conn: sqlite3.Connection, title: str, content: str) -> dict:
    """
    Yeni bir prompt ve ilk versiyonunu olusturur (atomic).

    Args:
        conn: SQLite baglantisi
        title: Prompt basligi
        content: Ilk versiyon icerigi

    Returns:
        Olusturulan prompt'un bilgileri (id, title, created_at, updated_at, version_count)
    """
    try:
        cursor = conn.execute(
            "INSERT INTO prompts (title) VALUES (?)",
            (title,)
        )
        prompt_id = cursor.lastrowid
        
        conn.execute(
            "INSERT INTO prompt_versions (prompt_id, version_no, content) VALUES (?, ?, ?)",
            (prompt_id, 1, content)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

    return get_prompt_by_id(conn, prompt_id)


def get_all_prompts(conn: sqlite3.Connection) -> list[dict]:
    """
    Tum prompt'lari listeler (en yeniler ustte).

    Args:
        conn: SQLite baglantisi

    Returns:
        Prompt listesi
    """
    rows = conn.execute(
        """
        SELECT p.id, p.title, p.created_at, p.updated_at, 
               (SELECT COUNT(*) FROM prompt_versions v WHERE v.prompt_id = p.id) as version_count 
        FROM prompts p ORDER BY p.created_at DESC
        """
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
        """
        SELECT p.id, p.title, p.created_at, p.updated_at,
               (SELECT COUNT(*) FROM prompt_versions v WHERE v.prompt_id = p.id) as version_count
        FROM prompts p WHERE p.id = ?
        """,
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
