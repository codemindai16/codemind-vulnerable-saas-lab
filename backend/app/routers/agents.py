from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.schemas import AgentTaskCreate, AgentTaskOut
from app.models import AgentTask, ProjectMember
from app.routers.auth import get_current_user
from app.services.agent_executor import AgentExecutor
from app.services.file_handler import FileHandler
from app.utils.security import sanitize_input

router = APIRouter(prefix="/agents", tags=["agents"])

class ScriptRunRequest(BaseModel):
    script: str

class FileOperationRequest(BaseModel):
    path: str
    content: str

@router.post("/run-script")
def run_script(
    req: ScriptRunRequest,
    current_user=Depends(get_current_user),
):
    executor = AgentExecutor()
    result = executor.execute_script(req.script)
    return {"ok": True, "result": result}

@router.post("/write-file")
def write_file(
    req: FileOperationRequest,
    current_user=Depends(get_current_user),
):
    sanitized_path = sanitize_input(req.path)
    handler = FileHandler()
    result = handler.write_file(sanitized_path, req.content)
    return {"ok": True, "result": result}

@router.post("/read-file")
def read_file(
    req: FileOperationRequest,
    current_user=Depends(get_current_user),
):
    sanitized_path = sanitize_input(req.path)
    handler = FileHandler()
    result = handler.read_file(sanitized_path)
    return {"ok": True, "result": result}

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
