import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models.tag import TagResponse, TagCreate
from app.services import tag_service

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("", response_model=list[TagResponse])
def list_tags(conn: sqlite3.Connection = Depends(get_db)):
    return tag_service.get_all_tags(conn)

@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(body: TagCreate, conn: sqlite3.Connection = Depends(get_db)):
    tag = tag_service.get_tag_by_name(conn, body.name.strip())
    if tag:
        # Upsert behavior: return existing if it already exists
        return tag
    
    try:
        cursor = conn.execute("INSERT INTO tags (name) VALUES (?)", (body.name.strip(),))
        conn.commit()
        return {"id": cursor.lastrowid, "name": body.name.strip()}
    except Exception as e:
        conn.rollback()
        raise e
