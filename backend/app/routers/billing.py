from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BillingCreate, BillingOut
from app.models import Billing
from app.routers.auth import get_current_user

router = APIRouter(prefix="/billing", tags=["billing"])

@router.post("/", response_model=BillingOut)
def create_billing(
    billing_data: BillingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    billing = Billing(
        user_id=current_user.id,
        amount=billing_data.amount,
        currency=billing_data.currency,
        description=billing_data.description,
    )
    db.add(billing)
    db.commit()
    db.refresh(billing)
    return billing

@router.get("/", response_model=list[BillingOut])
def list_billing(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Billing).filter(Billing.user_id == current_user.id).all()

@router.get("/summary")
def get_billing_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    billings = db.query(Billing).filter(Billing.user_id == current_user.id).all()
    total = sum(b.amount for b in billings)
    return {"total_amount": total, "currency": "USD", "count": len(billings)}

@router.put("/{billing_id}", response_model=BillingOut)
def update_billing(
    billing_id: int,
    billing_data: BillingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    billing = db.query(Billing).filter(
        Billing.id == billing_id,
        Billing.user_id == current_user.id,
    ).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing record not found")
    billing.amount = billing_data.amount
    billing.currency = billing_data.currency
    billing.description = billing_data.description
    db.commit()
    db.refresh(billing)
    return billing

@router.delete("/{billing_id}")
def delete_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    billing = db.query(Billing).filter(
        Billing.id == billing_id,
        Billing.user_id == current_user.id,
    ).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing record not found")
    db.delete(billing)
    db.commit()
    return {"ok": True}
