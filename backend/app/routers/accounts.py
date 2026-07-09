from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SocialAccountCreate, SocialAccountOut
from app.models import SocialAccount, SocialAccountMember, OrganizationMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/accounts", tags=["social-accounts"])


@router.post("/", response_model=SocialAccountOut)
def create_account(account_data: SocialAccountCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    membership = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == account_data.organization_id,
        OrganizationMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    account = SocialAccount(**account_data.dict())
    db.add(account)
    db.commit()
    db.refresh(account)
    member = SocialAccountMember(account_id=account.id, user_id=current_user.id, role="owner")
    db.add(member)
    db.commit()
    return account


@router.get("/", response_model=list[SocialAccountOut])
def list_accounts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    memberships = db.query(SocialAccountMember).filter(SocialAccountMember.user_id == current_user.id).all()
    account_ids = [m.account_id for m in memberships]
    return db.query(SocialAccount).filter(SocialAccount.id.in_(account_ids)).all()


@router.get("/{account_id}", response_model=SocialAccountOut)
def get_account(account_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    membership = db.query(SocialAccountMember).filter(SocialAccountMember.account_id == account_id, SocialAccountMember.user_id == current_user.id).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    return account
