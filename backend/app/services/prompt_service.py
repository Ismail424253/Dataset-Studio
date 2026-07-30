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
