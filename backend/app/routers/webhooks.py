from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SocialWebhookCreate, SocialWebhookOut
from app.models import SocialWebhook, SocialAccount, SocialAccountMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/{account_id}", response_model=SocialWebhookOut)
def create_webhook(
    account_id: int,
    webhook_data: SocialWebhookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(SocialAccountMember).filter(
        SocialAccountMember.account_id == account_id,
        SocialAccountMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    webhook = SocialWebhook(**webhook_data.dict(), account_id=account_id)
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


@router.get("/{account_id}", response_model=list[SocialWebhookOut])
def list_webhooks(
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
    return db.query(SocialWebhook).filter(SocialWebhook.account_id == account_id).all()
