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

@router.delete("/{org_id}/members/{user_id}")
def remove_member(org_id: int, user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    membership = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == org_id,
        OrganizationMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member")
    target = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == org_id,
        OrganizationMember.user_id == user_id,
    ).first()
    if not target:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(target)
    db.commit()
    return {"status": "removed"}

@router.delete("/{org_id}")
def delete_org(org_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    membership = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == org_id,
        OrganizationMember.user_id == current_user.id,
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member")
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.query(OrganizationMember).filter(OrganizationMember.organization_id == org_id).delete()
    db.delete(org)
    db.commit()
    return {"status": "deleted"}
