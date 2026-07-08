def test_ssrf_protection_exists():
    with open("app/services/webhook_executor.py") as f:
        content = f.read()

    protections = [
        "127.0.0.0",
        "10.0.0.0",
        "172.16.0.0",
        "192.168.0.0",
        "allowlist",
        "internal",
        "localhost",
    ]

    found = sum(1 for p in protections if p in content)
    assert found >= 1, "Webhook executor should have SSRF protection (internal IP blocking)"

def test_url_validation_before_request():
    with open("app/services/webhook_executor.py") as f:
        content = f.read()
    assert "url" in content.lower() and ("validate" in content.lower() or "check" in content.lower()), \
        "URL should be validated before making requests"
