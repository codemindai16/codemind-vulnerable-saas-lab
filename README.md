# CodeMind AI Security Benchmark Lab

A realistic vulnerable SaaS repository for testing autonomous code review, security validation and AI-generated fixes.

## Domain
AI Agent Task Manager - users create agents, run analysis tasks, upload files, configure webhooks, and manage billing.

## Tech Stack
- FastAPI + PostgreSQL + Redis
- Docker Compose
- pytest + bandit + ruff

## Branch Strategy (Demo Flow)
```
main                  -> secure baseline
vuln/sql-injection    -> SQL injection introduced
vuln/idor             -> broken access control introduced
vuln/ssrf             -> webhook SSRF introduced
vuln/path-traversal   -> unsafe file upload introduced
fix/sql-injection     -> expected fix
fix/idor              -> expected fix
```

## Quick Start
```bash
cp backend/.env.example backend/.env
docker compose up -d
```

## Security Testing
```bash
cd backend
pytest tests/ -v
bandit -r app/
ruff check app/
```

## Benchmark Ground Truth
See `vulnerabilities.yml` for deliberate vulnerabilities with CWE/OWASP mappings.
