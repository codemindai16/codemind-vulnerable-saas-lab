def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

class TestAuth:
    def test_register(self, client):
        resp = client.post("/auth/register", json={
            "email": "newuser@test.com",
            "password": "strongpass123",
            "full_name": "New User",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "newuser@test.com"
        assert data["full_name"] == "New User"
        assert "id" in data

    def test_register_duplicate_email(self, client):
        client.post("/auth/register", json={
            "email": "dup@test.com", "password": "pass123", "full_name": "Dup",
        })
        resp = client.post("/auth/register", json={
            "email": "dup@test.com", "password": "pass456", "full_name": "Dup2",
        })
        assert resp.status_code == 400

    def test_login_success(self, client):
        client.post("/auth/register", json={
            "email": "login@test.com", "password": "mypassword", "full_name": "Login",
        })
        resp = client.post("/auth/login", data={
            "username": "login@test.com", "password": "mypassword",
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_login_invalid_password(self, client):
        client.post("/auth/register", json={
            "email": "badpass@test.com", "password": "correctpass", "full_name": "BP",
        })
        resp = client.post("/auth/login", data={
            "username": "badpass@test.com", "password": "wrongpass",
        })
        assert resp.status_code == 401

class TestUsers:
    def test_get_me(self, client, auth_headers):
        resp = client.get("/users/me", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "test@example.com"

    def test_get_own_user(self, client, auth_headers):
        me = client.get("/users/me", headers=auth_headers).json()
        resp = client.get(f"/users/{me['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "test@example.com"

    def test_get_other_user_denied(self, client, auth_headers):
        client.post("/auth/register", json={
            "email": "other@test.com", "password": "pass123", "full_name": "Other",
        })
        other = client.post("/auth/login", data={
            "username": "other@test.com", "password": "pass123",
        }).json()
        other_headers = {"Authorization": f"Bearer {other['access_token']}"}
        me = client.get("/users/me", headers=auth_headers).json()

        resp = client.get(f"/users/{me['id']}", headers=other_headers)
        assert resp.status_code == 403

class TestOrganizations:
    def test_create_org(self, client, auth_headers):
        resp = client.post("/organizations/", json={
            "name": "My Org", "slug": "my-org",
        }, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "My Org"

    def test_list_orgs(self, client, auth_headers):
        client.post("/organizations/", json={
            "name": "Org1", "slug": "org1",
        }, headers=auth_headers)
        resp = client.get("/organizations/", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

class TestProjects:
    def test_create_project(self, client, auth_headers, sample_org):
        resp = client.post("/projects/", json={
            "name": "My Project",
            "description": "Desc",
            "organization_id": sample_org["id"],
        }, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "My Project"

    def test_list_projects(self, client, auth_headers, sample_project):
        resp = client.get("/projects/", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_project(self, client, auth_headers, sample_project):
        resp = client.get(f"/projects/{sample_project['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == sample_project["id"]

class TestBilling:
    def test_get_billing(self, client, auth_headers, sample_project):
        resp = client.get(f"/billing/{sample_project['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["plan"] == "free"

    def test_update_billing_plan(self, client, auth_headers, sample_project):
        resp = client.put(f"/billing/{sample_project['id']}", json={
            "plan": "pro",
            "usage_units": 100,
        }, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["plan"] == "pro"
        assert resp.json()["usage_units"] == 100

class TestFiles:
    def test_upload_file(self, client, auth_headers, sample_project, tmp_path):
        resp = client.post(
            f"/files/upload/{sample_project['id']}",
            files={"file": ("test.txt", b"hello world", "text/plain")},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["filename"] == "test.txt"

    def test_list_files(self, client, auth_headers, sample_project):
        client.post(
            f"/files/upload/{sample_project['id']}",
            files={"file": ("a.txt", b"aaa", "text/plain")},
            headers=auth_headers,
        )
        resp = client.get(f"/files/{sample_project['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

class TestWebhooks:
    def test_create_webhook(self, client, auth_headers, sample_project):
        resp = client.post(f"/webhooks/{sample_project['id']}", json={
            "url": "https://example.com/hook",
            "events": ["task.completed"],
        }, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["url"] == "https://example.com/hook"

    def test_list_webhooks(self, client, auth_headers, sample_project):
        client.post(f"/webhooks/{sample_project['id']}", json={
            "url": "https://example.com/hook2",
            "events": ["task.started"],
        }, headers=auth_headers)
        resp = client.get(f"/webhooks/{sample_project['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

class TestAgents:
    def test_create_task(self, client, auth_headers, sample_project):
        resp = client.post("/agents/tasks", json={
            "task_type": "code_review",
            "payload": {"repo": "test/repo"},
            "project_id": sample_project["id"],
        }, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["task_type"] == "code_review"
        assert resp.json()["status"] == "pending"

    def test_list_tasks(self, client, auth_headers, sample_project):
        client.post("/agents/tasks", json={
            "task_type": "analysis", "payload": {},
            "project_id": sample_project["id"],
        }, headers=auth_headers)
        resp = client.get("/agents/tasks", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_task(self, client, auth_headers, sample_project):
        created = client.post("/agents/tasks", json={
            "task_type": "scan", "payload": {},
            "project_id": sample_project["id"],
        }, headers=auth_headers).json()
        resp = client.get(f"/agents/tasks/{created['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

class TestAdmin:
    def test_admin_list_users_denied_for_non_admin(self, client, auth_headers):
        resp = client.get("/admin/users", headers=auth_headers)
        assert resp.status_code == 403

    def test_admin_list_tasks_denied_for_non_admin(self, client, auth_headers):
        resp = client.get("/admin/tasks", headers=auth_headers)
        assert resp.status_code == 403
