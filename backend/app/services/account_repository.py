from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models import SocialAccount


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_accounts(self, organization_id: int, search_term: str) -> list[SocialAccount]:
        query = text(
            "SELECT * FROM social_accounts WHERE organization_id = :org_id "
            "AND (account_username ILIKE :search OR display_name ILIKE :search OR bio ILIKE :search)"
        )
        result = self.db.execute(
            query,
            {"org_id": organization_id, "search": f"%{search_term}%"},
        )
        return [SocialAccount(**row._mapping) for row in result]

    def get_account_stats(self, account_id: int) -> dict:
        query = text("SELECT COUNT(*) as post_count FROM tracked_posts WHERE account_id = :aid")
        result = self.db.execute(query, {"aid": account_id}).fetchone()
        return {"post_count": result[0]} if result else {"post_count": 0}
