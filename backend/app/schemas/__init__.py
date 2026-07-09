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


class SocialAccountBase(BaseModel):
    platform: str = Field(description="twitter, instagram, linkedin, facebook, tiktok")
    account_username: str
    display_name: Optional[str] = None
    bio: Optional[str] = None


class SocialAccountCreate(SocialAccountBase):
    organization_id: int


class SocialAccountOut(SocialAccountBase):
    id: int
    organization_id: int
    is_tracking: bool
    last_synced: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class TrackedPostBase(BaseModel):
    post_id: Optional[str] = None
    content: Optional[str] = None
    author_username: Optional[str] = None
    author_display_name: Optional[str] = None
    platform: str
    posted_at: Optional[datetime] = None
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    engagement_score: float = 0.0
    metadata_json: Dict[str, Any] = {}


class TrackedPostOut(TrackedPostBase):
    id: int
    account_id: int
    fetched_at: datetime

    class Config:
        from_attributes = True


class SocialWebhookBase(BaseModel):
    url: str
    events: List[str] = []
    secret: Optional[str] = None


class SocialWebhookCreate(SocialWebhookBase):
    pass


class SocialWebhookOut(SocialWebhookBase):
    id: int
    account_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionBase(BaseModel):
    plan: str = "free"
    tracked_posts_limit: int = 100


class SubscriptionUpdate(BaseModel):
    plan: Optional[str] = None
    tracked_posts_limit: Optional[int] = None
    is_active: Optional[bool] = None


class SubscriptionOut(SubscriptionBase):
    id: int
    account_id: int
    price_per_month: float
    total_spent: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TrackingJobBase(BaseModel):
    job_type: str
    payload: Dict[str, Any] = {}
    account_id: int


class TrackingJobCreate(TrackingJobBase):
    pass


class TrackingJobOut(TrackingJobBase):
    id: int
    owner_id: int
    status: str
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
