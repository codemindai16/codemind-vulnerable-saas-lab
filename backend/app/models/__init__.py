from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default="member")
    created_at = Column(DateTime, default=datetime.utcnow)
    api_key = Column(String, unique=True, index=True)

    organizations = relationship("OrganizationMember", back_populates="user")
    accounts = relationship("SocialAccountMember", back_populates="user")
    tracking_jobs = relationship("TrackingJob", back_populates="owner")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    settings = Column(JSON, default={})

    members = relationship("OrganizationMember", back_populates="organization")
    social_accounts = relationship("SocialAccount", back_populates="organization")


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="member")
    joined_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organizations")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    display_name = Column(String)
    bio = Column(Text)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    is_tracking = Column(Boolean, default=True)
    last_synced = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="social_accounts")
    members = relationship("SocialAccountMember", back_populates="account")
    posts = relationship("TrackedPost", back_populates="account")
    webhooks = relationship("SocialWebhook", back_populates="account")
    billing = relationship("Subscription", back_populates="account", uselist=False)


class SocialAccountMember(Base):
    __tablename__ = "social_account_members"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="viewer")
    joined_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("SocialAccount", back_populates="members")
    user = relationship("User", back_populates="accounts")


class TrackedPost(Base):
    __tablename__ = "tracked_posts"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, index=True)
    content = Column(Text)
    author_username = Column(String)
    author_display_name = Column(String)
    platform = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    posted_at = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)
    metadata_json = Column(JSON, default={})

    account = relationship("SocialAccount", back_populates="posts")


class SocialWebhook(Base):
    __tablename__ = "social_webhooks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    events = Column(JSON, default=[])
    secret = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("SocialAccount", back_populates="webhooks")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    plan = Column(String, default="free")
    tracked_posts_limit = Column(Integer, default=100)
    price_per_month = Column(Float, default=0.0)
    total_spent = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("SocialAccount", back_populates="billing")


class TrackingJob(Base):
    __tablename__ = "tracking_jobs"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer)
    job_type = Column(String, nullable=False)
    payload = Column(JSON, default={})
    status = Column(String, default="pending")
    result = Column(JSON)
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    owner = relationship("User", back_populates="tracking_jobs")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    resource_type = Column(String)
    resource_id = Column(Integer)
    ip_address = Column(String)
    user_agent = Column(String)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
