from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BillingOut, BillingUpdate
from app.models import Billing, Project, ProjectMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/billing", tags=["billing"])

@router.get("/{project_id}", response_model=BillingOut)
def get_billing(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    billing = db.query(Billing).filter(Billing.project_id == project_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing not found")
    return billing

@router.put("/{project_id}", response_model=BillingOut)
def update_billing(
    project_id: int,
    billing_data: BillingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    billing = db.query(Billing).filter(Billing.project_id == project_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing not found")
    for key, value in billing_data.dict(exclude_unset=True).items():
        setattr(billing, key, value)
    db.commit()
    db.refresh(billing)
    return billing
