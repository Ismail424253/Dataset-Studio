import sqlite3
from typing import Optional

def get_all_tags(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, name FROM tags ORDER BY name ASC").fetchall()
    return [dict(row) for row in rows]

def get_tag_by_name(conn: sqlite3.Connection, name: str) -> Optional[dict]:
    row = conn.execute("SELECT id, name FROM tags WHERE name = ?", (name,)).fetchone()
    return dict(row) if row else None

def get_tag_by_id(conn: sqlite3.Connection, tag_id: int) -> Optional[dict]:
    row = conn.execute("SELECT id, name FROM tags WHERE id = ?", (tag_id,)).fetchone()
    return dict(row) if row else None

def get_tags_for_prompt(conn: sqlite3.Connection, prompt_id: int) -> list[dict]:
    rows = conn.execute(
        '''
        SELECT t.id, t.name 
        FROM tags t
        JOIN prompt_tags pt ON t.id = pt.tag_id
        WHERE pt.prompt_id = ?
        ORDER BY t.name ASC
        ''', 
        (prompt_id,)
    ).fetchall()
    return [dict(row) for row in rows]

def attach_tag_to_prompt(conn: sqlite3.Connection, prompt_id: int, tag_name: str) -> Optional[dict]:
    """
    Attach a tag to a prompt by name. Creates the tag if it doesn't exist (upsert).
    If it's already attached, it acts as a no-op (idempotent).
    """
    # Prompt check
    prompt = conn.execute("SELECT id FROM prompts WHERE id = ?", (prompt_id,)).fetchone()
    if not prompt:
        return None

    try:
        tag_name = tag_name.strip()
        # Find or create tag
        tag = get_tag_by_name(conn, tag_name)
        if not tag:
            cursor = conn.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
            tag_id = cursor.lastrowid
            tag = {"id": tag_id, "name": tag_name}
        else:
            tag_id = tag["id"]

        # Attach (ignore if already exists due to PRIMARY KEY(prompt_id, tag_id) or just select check)
        # Using INSERT OR IGNORE to handle duplicates gracefully
        conn.execute(
            "INSERT OR IGNORE INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)", 
            (prompt_id, tag_id)
        )
        conn.commit()
        return tag
    except Exception as e:
        conn.rollback()
        raise e

def remove_tag_from_prompt(conn: sqlite3.Connection, prompt_id: int, tag_id: int) -> bool:
    """Removes a tag from a prompt. Returns True if deleted, False if prompt/tag relation didn't exist."""
    cursor = conn.execute(
        "DELETE FROM prompt_tags WHERE prompt_id = ? AND tag_id = ?",
        (prompt_id, tag_id)
    )
    conn.commit()
    return cursor.rowcount > 0
