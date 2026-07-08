from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    role: str
    api_key: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class OrganizationBase(BaseModel):
    name: str
    slug: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: int
    owner_id: int
    created_at: datetime
    settings: Dict[str, Any] = {}

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    repo_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    organization_id: int

class ProjectOut(ProjectBase):
    id: int
    organization_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectFileBase(BaseModel):
    filename: str
    mime_type: Optional[str] = None

class ProjectFileOut(ProjectFileBase):
    id: int
    filepath: str
    project_id: int
    size: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class WebhookBase(BaseModel):
    url: str
    events: List[str] = []
    secret: Optional[str] = None

class WebhookCreate(WebhookBase):
    pass

class WebhookOut(WebhookBase):
    id: int
    project_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BillingBase(BaseModel):
    plan: str = "free"
    usage_units: int = 0

class BillingUpdate(BaseModel):
    plan: Optional[str] = None
    usage_units: Optional[int] = None
    is_active: Optional[bool] = None

class BillingOut(BillingBase):
    id: int
    project_id: int
    price_per_unit: float
    total_spent: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AgentTaskBase(BaseModel):
    task_type: str
    payload: Dict[str, Any] = {}
    project_id: int

class AgentTaskCreate(AgentTaskBase):
    pass

class AgentTaskOut(AgentTaskBase):
    id: int
    owner_id: int
    status: str
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
