from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import OrganizationCreate, OrganizationOut
from app.models import Organization, OrganizationMember
from app.routers.auth import get_current_user

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("/", response_model=OrganizationOut)
def create_org(org_data: OrganizationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    org = Organization(**org_data.dict(), owner_id=current_user.id)
    db.add(org)
    db.commit()
    db.refresh(org)
    member = OrganizationMember(organization_id=org.id, user_id=current_user.id, role="owner")
    db.add(member)
    db.commit()
    return org

@router.get("/", response_model=list[OrganizationOut])
def list_orgs(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    memberships = db.query(OrganizationMember).filter(OrganizationMember.user_id == current_user.id).all()
    org_ids = [m.organization_id for m in memberships]
    return db.query(Organization).filter(Organization.id.in_(org_ids)).all()
