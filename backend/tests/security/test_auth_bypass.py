from app.utils.auth import verify_password, get_password_hash
from app.config import settings

def test_password_verified_on_login():
    with open("app/routers/auth.py") as f:
        content = f.read()
    assert "verify_password" in content, "Login endpoint must call verify_password()"
    assert "form_data.password" in content or "user_data.password" in content, \
        "Login must check the provided password against stored hash"

def test_password_hashing_used():
    password = "test-pass-123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed), "Password hash/verify cycle should work"
    assert not verify_password("wrong-pass", hashed), "Wrong password should not verify"
