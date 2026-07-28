"""
AI Prompt & Dataset Studio — Veritabanı Başlatma Scripti

Bu script:
  1. backend/database/app.db SQLite veritabanı dosyasını oluşturur (yoksa).
  2. schema.sql dosyasındaki CREATE TABLE ifadelerini çalıştırır.
  3. Tüm tabloların başarıyla oluşturulduğunu doğrular.

Güvenle tekrar çalıştırılabilir (CREATE TABLE IF NOT EXISTS kullanılır).

Kullanım:
    python backend/database/init_db.py
"""

import sqlite3
import os
import sys


# Dosya yollarını belirle
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "app.db")
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "schema.sql")

# Beklenen tablo listesi (doğrulama için)
EXPECTED_TABLES = [
    "prompts",
    "prompt_versions",
    "tags",
    "prompt_tags",
    "datasets",
    "dataset_items",
]


def init_db():
    """Veritabanını oluştur ve şemayı uygula."""

    # schema.sql dosyasını oku
    if not os.path.exists(SCHEMA_PATH):
        print(f"HATA: Şema dosyası bulunamadı: {SCHEMA_PATH}")
        sys.exit(1)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Veritabanına bağlan (dosya yoksa otomatik oluşturulur)
    print(f"Veritabanı dosyası: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    try:
        # Foreign key desteğini etkinleştir
        conn.execute("PRAGMA foreign_keys = ON;")

        # Şemayı uygula
        conn.executescript(schema_sql)
        conn.commit()
        print("Şema başarıyla uygulandı.")

        # Oluşturulan tabloları doğrula
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        )
        created_tables = [row[0] for row in cursor.fetchall()]

        print(f"\nOluşturulan tablolar ({len(created_tables)} adet):")
        for table_name in created_tables:
            # Her tablonun sütun bilgilerini göster
            col_cursor = conn.execute(f"PRAGMA table_info({table_name});")
            columns = col_cursor.fetchall()
            col_names = [col[1] for col in columns]
            print(f"  [OK] {table_name} ({', '.join(col_names)})")

        # Beklenen tabloların hepsinin oluşturulduğunu kontrol et
        missing = set(EXPECTED_TABLES) - set(created_tables)
        if missing:
            print(f"\nUYARI: Eksik tablolar: {', '.join(missing)}")
            sys.exit(1)
        else:
            print(f"\nTum {len(EXPECTED_TABLES)} tablo basariyla olusturuldu.")

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
