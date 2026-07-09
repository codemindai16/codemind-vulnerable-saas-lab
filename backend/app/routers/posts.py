from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TrackedPostOut
from app.models import TrackedPost, SocialAccountMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["tracked-posts"])


@router.get("/{account_id}", response_model=list[TrackedPostOut])
def list_posts(
    account_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(SocialAccountMember).filter(
        SocialAccountMember.account_id == account_id,
        SocialAccountMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.query(TrackedPost).filter(TrackedPost.account_id == account_id).all()
