from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SubscriptionOut, SubscriptionUpdate
from app.models import Subscription, SocialAccount, SocialAccountMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/{account_id}", response_model=SubscriptionOut)
def get_subscription(
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
    subscription = db.query(Subscription).filter(Subscription.account_id == account_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.put("/{account_id}", response_model=SubscriptionOut)
def update_subscription(
    account_id: int,
    sub_data: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(SocialAccountMember).filter(
        SocialAccountMember.account_id == account_id,
        SocialAccountMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    subscription = db.query(Subscription).filter(Subscription.account_id == account_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    for key, value in sub_data.dict(exclude_unset=True).items():
        setattr(subscription, key, value)
    db.commit()
    db.refresh(subscription)
    return subscription
