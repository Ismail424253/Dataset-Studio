-- ============================================================
-- AI Prompt & Dataset Studio — Veritabanı Şeması
-- SQLite için CREATE TABLE ifadeleri
-- ============================================================

-- Foreign key desteğini etkinleştir (SQLite'da varsayılan olarak kapalıdır)
PRAGMA foreign_keys = ON;

-- 1. Prompt Kayıtları
CREATE TABLE IF NOT EXISTS prompts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 2. Prompt Versiyonları
CREATE TABLE IF NOT EXISTS prompt_versions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id   INTEGER NOT NULL,
    version_no  INTEGER NOT NULL,
    content     TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),

    UNIQUE (prompt_id, version_no),
    FOREIGN KEY (prompt_id) REFERENCES prompts (id) ON DELETE CASCADE
);

-- 3. Etiketler
CREATE TABLE IF NOT EXISTS tags (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT    NOT NULL UNIQUE
);

-- 4. Prompt-Etiket İlişkisi (Çoka-Çok)
CREATE TABLE IF NOT EXISTS prompt_tags (
    prompt_id  INTEGER NOT NULL,
    tag_id     INTEGER NOT NULL,

    PRIMARY KEY (prompt_id, tag_id),
    FOREIGN KEY (prompt_id) REFERENCES prompts (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)    REFERENCES tags (id)    ON DELETE CASCADE
);

-- 5. Veri Setleri
CREATE TABLE IF NOT EXISTS datasets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    description  TEXT,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 6. Veri Seti Öğeleri
CREATE TABLE IF NOT EXISTS dataset_items (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id         INTEGER NOT NULL,
    prompt_version_id  INTEGER NOT NULL,
    output_text        TEXT    NOT NULL,

    FOREIGN KEY (dataset_id)        REFERENCES datasets (id)        ON DELETE CASCADE,
    FOREIGN KEY (prompt_version_id) REFERENCES prompt_versions (id) ON DELETE RESTRICT
);
