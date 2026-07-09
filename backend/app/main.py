from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, users, organizations, accounts, posts, webhooks, billing, tracking, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SocialTracker SaaS Lab",
    description="Social media tracking & analytics platform - Benchmark repository for AI security testing",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organizations.router)
app.include_router(accounts.router)
app.include_router(posts.router)
app.include_router(webhooks.router)
app.include_router(billing.router)
app.include_router(tracking.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok"}
