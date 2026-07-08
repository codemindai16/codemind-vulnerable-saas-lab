# CodeMind AI Security Benchmark Lab

A realistic vulnerable SaaS repository for benchmarking autonomous code review, security validation, and AI-generated fixes.

**Domain**: AI Agent Task Manager — users create agents, run analysis tasks, upload files, configure webhooks, and manage billing.

---

## Quick Start

```bash
cp backend/.env.example backend/.env
docker compose up -d
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI (Python 3.11) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Auth | JWT (python-jose) + bcrypt |
| Testing | pytest, httpx |
| Linting | ruff, mypy |
| SAST | bandit |
| CI | GitHub Actions |

---

## Vulnerability Inventory

| ID | Title | OWASP | CWE | Severity | Branch |
|----|-------|-------|-----|----------|--------|
| CMD-SEC-001 | Weak JWT Secret Key | A02 Cryptographic Failures | CWE-321 | Critical | main |
| CMD-SEC-002 | Excessive JWT Token Expiration | A07 Identification Failures | CWE-613 | High | main |
| CMD-SEC-003 | Missing Password Verification in Login | A07 Identification Failures | CWE-287 | Critical | main |
| CMD-SEC-004 | API Key Exposed in User Response | A04 Insecure Design | CWE-200 | High | main |
| CMD-SEC-005 | Security Credentials in Log Output | A09 Logging Failures | CWE-532 | Medium | main |
| CMD-SEC-006 | CORS Allows All Origins | A05 Security Misconfiguration | CWE-942 | Medium | main |
| CMD-SEC-007 | SQL Injection in Project Search | A03 Injection | CWE-89 | Critical | vuln/sql-injection |
| CMD-SEC-008 | IDOR in User Details | A01 Broken Access Control | CWE-639 | High | vuln/idor |
| CMD-SEC-009 | SSRF in Webhook Handler | A10 SSRF | CWE-918 | High | vuln/ssrf |
| CMD-SEC-010 | Path Traversal in File Upload | A01 Broken Access Control | CWE-22 | High | vuln/path-traversal |
| CMD-SEC-011 | Mass Assignment in Billing | A01 Broken Access Control | CWE-915 | Medium | vuln/mass-assignment |
| CMD-SEC-012 | Unsafe Command Execution | A03 Injection | CWE-78 | Critical | vuln/command-injection |

Full ground truth: [vulnerabilities.yml](vulnerabilities.yml)

---

## Branch Strategy

```
main                         Secure baseline (6 config-level vulns)
│
├── vuln/sql-injection       SQL injection via string interpolation
├── vuln/idor                Missing authorization check
├── vuln/ssrf                No URL validation in webhook
├── vuln/path-traversal      Unsafe filename handling
├── vuln/mass-assignment     Protected billing fields exposed
├── vuln/command-injection   shell=True in subprocess
│
└── fix/*                    Expected fix for each vuln
```

Each `vuln/*` branch has a corresponding `fix/*` branch with the secure version.

---

## CodeMind AI Benchmark Flow

1. Create a PR from `vuln/*` into `main`
2. CodeMind AI analyzes the diff
3. Security Agent detects the vulnerability
4. Architecture Agent assesses impact
5. Sandbox runs security tests
6. Fix patch is generated
7. Regression tests pass
8. Final report is produced

### Example: SSRF Demo

```
PR: Add webhook trigger endpoint
    ↓
CodeMind AI detects user-controlled URL reaching requests.post()
    ↓
Risk: SSRF to internal services (High severity)
    ↓
Fix: Add URL allowlist + block internal IP ranges
    ↓
Validation: test_ssrf.py confirms protection
```

---

## Security Testing

```bash
cd backend

# Unit & integration tests
pytest tests/ -v

# Security-specific tests
pytest tests/security/ -v

# SAST baseline
bandit -r app/ -f json

# Linting
ruff check app/ tests/
mypy app/ --ignore-missing-imports
```

## Benchmark Results

See [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md) for the latest evaluation.

| Metric | Description |
|--------|-------------|
| Detection Rate | Vulnerabilities correctly identified |
| Classification | Correct CWE/OWASP mapping and severity |
| Fix Accuracy | Patch resolves the issue |
| Test Pass Rate | All security tests pass after fix |
| False Positives | Incorrect flags reported |

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              FastAPI entry point
│   │   ├── config.py            Settings (DELIBERATE VULNS)
│   │   ├── database.py          SQLAlchemy engine
│   │   ├── models/              SQLAlchemy models
│   │   ├── routers/             API endpoints
│   │   │   ├── auth.py          Registration/login
│   │   │   ├── users.py         User profiles
│   │   │   ├── organizations.py Org management
│   │   │   ├── projects.py      Project CRUD
│   │   │   ├── files.py         File upload/download
│   │   │   ├── webhooks.py      Webhook config
│   │   │   ├── billing.py       Billing & usage
│   │   │   ├── agents.py        Agent task management
│   │   │   └── admin.py         Admin panel
│   │   ├── schemas/             Pydantic models
│   │   ├── services/            Business logic layer
│   │   └── utils/               Auth, logging
│   ├── tests/
│   │   ├── conftest.py          Fixtures
│   │   ├── test_api.py          Integration tests
│   │   └── security/            Per-vuln validation tests
│   └── Dockerfile
├── docker-compose.yml
├── vulnerabilities.yml          Ground truth
└── BENCHMARK_RESULTS.md         Evaluation template
```

---

## License

MIT — Use for benchmarking, education, and research.
