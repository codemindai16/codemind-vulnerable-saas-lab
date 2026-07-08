def test_logs_do_not_contain_credentials():
    with open("app/utils/security.py") as f:
        content = f.read()
    assert "api_key=" not in content or "redact" in content or "mask" in content, \
        "Logs should not expose raw api_key; use redaction"
    assert "token=" not in content or "redact" in content or "mask" in content, \
        "Logs should not expose raw token; use redaction"
