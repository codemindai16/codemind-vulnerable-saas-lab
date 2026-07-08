from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_projects(self, organization_id: int, search_term: str) -> list[Project]:
        query = text(
            f"SELECT * FROM projects WHERE organization_id = {organization_id} "
            f"AND (name LIKE '%{search_term}%' OR description LIKE '%{search_term}%')"
        )
        result = self.db.execute(query)
        return [Project(**row._mapping) for row in result]

    def get_project_stats(self, project_id: int) -> dict:
        query = text(f"SELECT COUNT(*) as file_count FROM project_files WHERE project_id = {project_id}")
        result = self.db.execute(query).fetchone()
        return {"file_count": result[0]} if result else {"file_count": 0}
