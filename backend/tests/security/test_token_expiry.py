from app.config import settings

def test_token_expiry_reasonable():
    max_allowed = 60  # 60 minutes max
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES <= max_allowed, \
        f"Token expiry {settings.ACCESS_TOKEN_EXPIRE_MINUTES}min exceeds {max_allowed}min limit"

def test_token_expiry_not_excessive():
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES < 1440, \
        "Token expiry should be less than 24 hours (1440 minutes)"
