"""
Versiyon servisi — versiyonlarla ilgili veritabani islemleri.
"""

import sqlite3
from typing import Optional


def add_version(conn: sqlite3.Connection, prompt_id: int, content: str) -> Optional[dict]:
    """
    Mevcut bir prompt'a yeni bir versiyon ekler.
    
    Args:
        conn: SQLite baglantisi
        prompt_id: Prompt id
        content: Versiyon icerigi
        
    Returns:
        Olusturulan versiyonun bilgileri veya None (prompt bulunamazsa)
    """
    # Prompt'un var olup olmadigini kontrol et
    prompt = conn.execute("SELECT id FROM prompts WHERE id = ?", (prompt_id,)).fetchone()
    if not prompt:
        return None
        
    try:
        # Mevcut en yuksek versiyon numarasini bul
        row = conn.execute("SELECT MAX(version_no) as max_v FROM prompt_versions WHERE prompt_id = ?", (prompt_id,)).fetchone()
        next_v = (row['max_v'] or 0) + 1
        
        # Yeni versiyonu ekle
        cursor = conn.execute(
            "INSERT INTO prompt_versions (prompt_id, version_no, content) VALUES (?, ?, ?)",
            (prompt_id, next_v, content)
        )
        
        # Parent prompt'un updated_at alanini guncelle
        conn.execute("UPDATE prompts SET updated_at = datetime('now') WHERE id = ?", (prompt_id,))
        conn.commit()
        
        return get_version(conn, prompt_id, next_v)
    except Exception as e:
        conn.rollback()
        raise e


def get_versions(conn: sqlite3.Connection, prompt_id: int) -> list[dict]:
    """
    Bir prompt'un tum versiyonlarini artan sirada getirir.
    """
    rows = conn.execute(
        "SELECT id, prompt_id, version_no, content, created_at FROM prompt_versions WHERE prompt_id = ? ORDER BY version_no ASC",
        (prompt_id,)
    ).fetchall()
    return [dict(row) for row in rows]


def get_version(conn: sqlite3.Connection, prompt_id: int, version_no: int) -> Optional[dict]:
    """
    Belirli bir prompt'un belirli bir versiyonunu getirir.
    """
    row = conn.execute(
        "SELECT id, prompt_id, version_no, content, created_at FROM prompt_versions WHERE prompt_id = ? AND version_no = ?",
        (prompt_id, version_no)
    ).fetchone()
    return dict(row) if row else None
