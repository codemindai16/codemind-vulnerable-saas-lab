from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserOut
from app.models import User, TrackingJob, AuditLog
from app.routers.auth import get_current_user
from app.schemas import TrackingJobOut
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current_user=Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/users", response_model=list[UserOut])
def list_all_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return db.query(User).all()


@router.get("/jobs", response_model=list[TrackingJobOut])
def list_all_jobs(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return db.query(TrackingJob).all()


class AuditLogOut(BaseModel):
    id: int
    user_id: int
    action: str
    resource_type: Optional[str]
    resource_id: Optional[int]
    ip_address: Optional[str]
    metadata: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/audit-logs", response_model=list[AuditLogOut])
def list_audit_logs(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
