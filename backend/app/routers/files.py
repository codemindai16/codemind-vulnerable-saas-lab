import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ProjectFileOut
from app.models import Project, ProjectFile, ProjectMember
from app.routers.auth import get_current_user
from app.config import settings
from app.services.file_handler import FileHandler

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload/{project_id}", response_model=ProjectFileOut)
async def upload_file(
    project_id: int,
    file: UploadFile = File(...),
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

    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_file = ProjectFile(
        filename=file.filename,
        filepath=filepath,
        project_id=project_id,
        uploaded_by=current_user.id,
        size=os.path.getsize(filepath),
        mime_type=file.content_type,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.get("/{project_id}", response_model=list[ProjectFileOut])
def list_files(
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
    return db.query(ProjectFile).filter(ProjectFile.project_id == project_id).all()

@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
):
    db_file = db.query(ProjectFile).filter(ProjectFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    handler = FileHandler()
    content = handler.read_file(db_file.filename)
    from fastapi.responses import Response
    return Response(content=content, media_type=db_file.mime_type or "application/octet-stream")
