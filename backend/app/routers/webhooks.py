from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import WebhookCreate, WebhookOut
from app.models import Webhook, Project, ProjectMember
from app.routers.auth import get_current_user
from app.services.webhook_executor import WebhookExecutor

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/{project_id}", response_model=WebhookOut)
def create_webhook(
    project_id: int,
    webhook_data: WebhookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    webhook = Webhook(**webhook_data.dict(), project_id=project_id)
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook

@router.get("/{project_id}", response_model=list[WebhookOut])
def list_webhooks(
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
    return db.query(Webhook).filter(Webhook.project_id == project_id).all()

@router.post("/trigger/{webhook_id}")
def trigger_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    executor = WebhookExecutor()
    result = executor.execute(webhook.url, {"event": "test", "user_id": current_user.id})
    return result
