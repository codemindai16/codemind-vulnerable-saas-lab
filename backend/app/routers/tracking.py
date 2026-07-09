from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TrackingJobCreate, TrackingJobOut
from app.models import TrackingJob, SocialAccountMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/tracking", tags=["tracking-jobs"])


@router.post("/jobs", response_model=TrackingJobOut)
def create_job(
    job_data: TrackingJobCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(SocialAccountMember).filter(
        SocialAccountMember.account_id == job_data.account_id,
        SocialAccountMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    job = TrackingJob(
        owner_id=current_user.id,
        account_id=job_data.account_id,
        job_type=job_data.job_type,
        payload=job_data.payload,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/jobs", response_model=list[TrackingJobOut])
def list_jobs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(TrackingJob).filter(TrackingJob.owner_id == current_user.id).all()


@router.get("/jobs/{job_id}", response_model=TrackingJobOut)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = db.query(TrackingJob).filter(
        TrackingJob.id == job_id,
        TrackingJob.owner_id == current_user.id,
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Tracking job not found")
    return job
