from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemRead

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.get("/")
def list_action_items(
    page: int | None = None, 
    page_size: int | None = None, 
    db: Session = Depends(get_db)
):
    # If no pagination parameters are requested, return plain list to keep existing tests happy
    if page is None and page_size is None:
        rows = db.execute(select(ActionItem)).scalars().all()
        return [ActionItemRead.model_validate(row) for row in rows]

    # Standardize parameters if they are provided
    p = max(1, page or 1)
    ps = max(1, page_size or 10)
    offset = (p - 1) * ps

    total = db.query(ActionItem).count()
    rows = db.execute(
        select(ActionItem).offset(offset).limit(ps)
    ).scalars().all()
    
    items = [ActionItemRead.model_validate(row) for row in rows]

    return {
        "items": items,
        "total": total,
        "page": p,
        "page_size": ps
    }


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_action_item(
    payload: ActionItemCreate, db: Session = Depends(get_db)
) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_action_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)
