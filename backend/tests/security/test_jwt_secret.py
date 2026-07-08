from app.config import settings

def test_jwt_secret_not_hardcoded_weak():
    assert settings.SECRET_KEY != "weak-secret-key-123", "JWT secret is still the default weak key"
    assert len(settings.SECRET_KEY) >= 32, "JWT secret should be at least 256 bits (32 chars)"

def test_jwt_secret_not_in_source_code():
    with open("app/config.py") as f:
        content = f.read()
    assert "weak-secret-key" not in content, "Weak secret key found in source code"
