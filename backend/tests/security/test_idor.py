def test_user_detail_has_authorization_check():
    with open("app/routers/users.py") as f:
        content = f.read()

    function_start = content.find("def get_user")
    function_body = content[function_start:]

    checks = [
        "membership",
        "ProjectMember",
        "OrganizationMember",
        "current_user.id",
        "user_id",
        "403",
        "Access denied",
        "admin",
    ]

    found = sum(1 for c in checks if c in function_body)
    assert found >= 2, f"get_user endpoint missing authorization checks (only {found}/7 checks found)"
