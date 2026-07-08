from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ProjectCreate, ProjectOut
from app.models import Project, ProjectMember, OrganizationMember
from app.routers.auth import get_current_user
from app.services.project_repository import ProjectRepository

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectOut)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    membership = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == project_data.organization_id,
        OrganizationMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    project = Project(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    member = ProjectMember(project_id=project.id, user_id=current_user.id, role="owner")
    db.add(member)
    db.commit()
    return project

@router.get("/", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    memberships = db.query(ProjectMember).filter(ProjectMember.user_id == current_user.id).all()
    project_ids = [m.project_id for m in memberships]
    return db.query(Project).filter(Project.id.in_(project_ids)).all()

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    membership = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == current_user.id).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/search/{organization_id}")
def search_projects(organization_id: int, q: str = Query(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = ProjectRepository(db)
    results = repo.search_projects(organization_id, q)
    return results
