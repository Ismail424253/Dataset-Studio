"""
AI Prompt & Dataset Studio — Veritabani baglanti yonetimi.

SQLite veritabanina baglanti saglayan yardimci fonksiyonlar.
Python standart kutuphanesindeki sqlite3 modulu kullanilir.
"""

import sqlite3
import os

# Veritabani dosya yolu (backend/database/app.db)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(_BASE_DIR, "database", "app.db")


def get_connection() -> sqlite3.Connection:
    """
    SQLite veritabanina yeni bir baglanti acar.

    - Foreign key destegi etkinlestirilir.
    - Row factory olarak sqlite3.Row kullanilir (satirlara dict-benzeri erisim).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """
    FastAPI dependency olarak kullanilir.
    Her request icin bir baglanti acar, islem bitince kapatir.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
