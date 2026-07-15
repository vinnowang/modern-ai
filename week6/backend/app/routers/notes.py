from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note
from ..schemas import NoteCreate, NoteRead
from ..services.extract import extract_action_items

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/")
def list_notes(
    page: int | None = None, 
    page_size: int | None = None, 
    db: Session = Depends(get_db)
):
    # If no pagination parameters are requested, return plain list to keep existing tests happy
    if page is None and page_size is None:
        rows = db.execute(select(Note)).scalars().all()
        return [NoteRead.model_validate(row) for row in rows]

    # Standardize parameters if they are provided
    p = max(1, page or 1)
    ps = max(1, page_size or 10)
    offset = (p - 1) * ps

    total = db.query(Note).count()
    rows = db.execute(
        select(Note).offset(offset).limit(ps)
    ).scalars().all()
    
    items = [NoteRead.model_validate(row) for row in rows]
    
    return {
        "items": items,
        "total": total,
        "page": p,
        "page_size": ps
    }


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()

    extracted_tasks = extract_action_items(payload.content)
    for task_desc in extracted_tasks:
        action = ActionItem(description=task_desc, completed=False)
        db.add(action)

    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search/", response_model=list[NoteRead])
def search_notes(q: str | None = None, db: Session = Depends(get_db)) -> list[NoteRead]:
    if not q:
        rows = db.execute(select(Note)).scalars().all()
    else:
        rows = (
            db.execute(select(Note).where(Note.title.ilike(f"%{q}%") | Note.content.ilike(f"%{q}%")))
            .scalars()
            .all()
        )
    return [NoteRead.model_validate(row) for row in rows]
