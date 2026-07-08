def test_cors_not_wildcard():
    with open("app/main.py") as f:
        content = f.read()
    assert '["*"]' not in content or "allow_origins" not in content, \
        "CORS should not allow all origins with wildcard"
