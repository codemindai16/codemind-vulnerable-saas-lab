def test_password_hashing_uses_bcrypt():
    with open("app/utils/auth.py") as f:
        content = f.read()
    assert "bcrypt" in content or "CryptContext" in content, \
        "Password hashing should use bcrypt, not MD5/SHA1"
    assert "md5" not in content, "MD5 should not be used for password hashing"

def test_no_md5_for_passwords():
    with open("app/utils/auth.py") as f:
        content = f.read()
    assert "hashlib" not in content or "digest" not in content or "md5" not in content, \
        "MD5 should not be used anywhere in password handling"
