# CodeMind AI Demo: SSRF Detection & Fix

## Scenario

A developer adds a webhook trigger feature that lets users POST to any URL.
The code uses `requests.post(url, ...)` without validating the target,
creating a Server-Side Request Forgery (SSRF) vulnerability.

## Step-by-Step Demo

### 1. Create PR from `vuln/ssrf` into `main`

```
git checkout -b demo/ssrf-demo main
git merge vuln/ssrf --no-commit --no-ff
```

### 2. CodeMind AI Analysis

CodeMind AI scans the diff and detects:

```
🚨 SSRF Vulnerability Found
File: backend/app/services/webhook_executor.py
Risk: User-controlled URL passed directly to requests.post()
Impact: Attacker can scan internal network, access cloud metadata endpoints
Severity: HIGH (CWE-918, OWASP A10)
```

### 3. Fix Applied

CodeMind AI generates a patch:

```diff
+ import ipaddress
+ from urllib.parse import urlparse
+ 
+ BLOCKED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "::1"]
+ BLOCKED_NETWORKS = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
+ 
  def execute(self, url: str, payload: dict, secret: str = None) -> dict:
+     parsed = urlparse(url)
+     if self._is_internal(parsed.hostname):
+         raise ValueError("SSRF blocked")
+     if parsed.scheme not in ("https",):
+         raise ValueError("Only HTTPS allowed")
      headers = {"Content-Type": "application/json"}
      response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
```

### 4. Validation

```bash
pytest tests/security/test_ssrf.py -v
# ✓ test_ssrf_protection_exists PASSED
# ✓ test_url_validation_before_request PASSED
```

### 5. Final Report

| Check | Result |
|-------|--------|
| Vulnerability detected | ✅ |
| Correct file identified | ✅ |
| Risk assessed correctly | ✅ |
| Fix resolves the issue | ✅ |
| Security test passes | ✅ |
| No regression | ✅ |
