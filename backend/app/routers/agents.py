from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AgentTaskCreate, AgentTaskOut
from app.models import AgentTask, ProjectMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("/tasks", response_model=AgentTaskOut)
def create_task(
    task_data: AgentTaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == task_data.project_id,
        ProjectMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    task = AgentTask(
        owner_id=current_user.id,
        project_id=task_data.project_id,
        task_type=task_data.task_type,
        payload=task_data.payload,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/tasks", response_model=list[AgentTaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(AgentTask).filter(AgentTask.owner_id == current_user.id).all()

@router.get("/tasks/{task_id}", response_model=AgentTaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = db.query(AgentTask).filter(
        AgentTask.id == task_id,
        AgentTask.owner_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
