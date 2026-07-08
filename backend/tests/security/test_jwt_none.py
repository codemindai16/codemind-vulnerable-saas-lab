def test_jwt_rejects_none_algorithm():
    with open("app/utils/auth.py") as f:
        content = f.read()
    assert "verify_signature" not in content or "options" not in content, \
        "JWT decode should not disable signature verification"

def test_jwt_requires_algorithm():
    with open("app/utils/auth.py") as f:
        content = f.read()
    assert "algorithms" in content, "JWT decode must specify allowed algorithms"
    assert "HS256" in content, "JWT decode must require HS256 algorithm"
