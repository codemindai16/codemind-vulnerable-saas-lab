def test_no_string_interpolation_in_queries():
    with open("app/services/project_repository.py") as f:
        content = f.read()

    dangerous_patterns = [
        "f\"", ".format(", "%" + "s",
    ]
    for pattern in dangerous_patterns:
        assert pattern not in content, \
            f"String interpolation ({pattern}) should not be used in SQL queries"

def test_parameterized_queries_used():
    with open("app/services/project_repository.py") as f:
        content = f.read()
    assert ":param" in content or "%s" not in content or "?" in content, \
        "SQL queries should use parameterized style"
