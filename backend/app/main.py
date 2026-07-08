from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, users, organizations, projects, files, webhooks, billing, agents, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CodeMind Vulnerable SaaS Lab",
    description="AI-powered code review benchmark repository - AI Agent Task Manager",
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
app.include_router(projects.router)
app.include_router(files.router)
app.include_router(webhooks.router)
app.include_router(billing.router)
app.include_router(agents.router)
app.include_router(admin.router)

@app.get("/health")
def health():
    return {"status": "ok"}
