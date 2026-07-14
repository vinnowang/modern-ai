from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemRead

router = APIRouter(prefix="/action-items", tags=["action_items"])


class BulkCompletePayload(BaseModel):
    ids: list[int]


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    completed: bool | None = None, db: Session = Depends(get_db)
) -> list[ActionItemRead]:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed == completed)
    rows = db.execute(stmt).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.post("/bulk-complete")
def bulk_complete(payload: BulkCompletePayload, db: Session = Depends(get_db)):
    if not payload.ids:
        return {"message": "No IDs provided"}

    # Run inside a clean transaction context
    try:
        stmt = update(ActionItem).where(ActionItem.id.in_(payload.ids)).values(completed=True)
        db.execute(stmt)
        db.commit()  # Explicitly commit the transactional batch change
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}") from e

    return {"message": f"Successfully completed {len(payload.ids)} items"}
