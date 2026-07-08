def test_filename_sanitized():
    with open("app/services/file_handler.py") as f:
        content = f.read()

    sanitizers = [
        "basename",
        "sanitize",
        "secure_filename",
        "uuid",
        "replace",
        "strip",
    ]

    found = sum(1 for s in sanitizers if s in content)
    assert found >= 1, "File handler should sanitize filenames to prevent path traversal"

def test_no_direct_user_filename_in_path():
    with open("app/services/file_handler.py") as f:
        content = f.read()
    assert "file.filename" not in content or "basename" in content or "uuid" in content, \
        "User-supplied filename should not be used directly in filepath"
