import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.config import settings

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_headers(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
    })
    resp = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "testpass123",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def admin_headers(client):
    client.post("/auth/register", json={
        "email": "admin@example.com",
        "password": "adminpass123",
        "full_name": "Admin User",
    })
    resp = client.post("/auth/login", data={
        "username": "admin@example.com",
        "password": "adminpass123",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def sample_org(client, auth_headers):
    resp = client.post("/organizations/", json={
        "name": "Test Org",
        "slug": "test-org",
    }, headers=auth_headers)
    return resp.json()

@pytest.fixture(scope="function")
def sample_project(client, auth_headers, sample_org):
    resp = client.post("/projects/", json={
        "name": "Test Project",
        "description": "A test project",
        "organization_id": sample_org["id"],
    }, headers=auth_headers)
    return resp.json()
