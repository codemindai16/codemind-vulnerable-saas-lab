from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_projects(self, organization_id: int, search_term: str) -> list[Project]:
        query = text(
            "SELECT * FROM projects WHERE organization_id = :org_id "
            "AND (name ILIKE :search OR description ILIKE :search)"
        )
        result = self.db.execute(
            query,
            {"org_id": organization_id, "search": f"%{search_term}%"},
        )
        return [Project(**row._mapping) for row in result]

    def get_project_stats(self, project_id: int) -> dict:
        query = text("SELECT COUNT(*) as file_count FROM project_files WHERE project_id = :pid")
        result = self.db.execute(query, {"pid": project_id}).fetchone()
        return {"file_count": result[0]} if result else {"file_count": 0}
