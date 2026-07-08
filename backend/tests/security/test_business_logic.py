def test_org_delete_requires_owner():
    with open("app/routers/organizations.py") as f:
        content = f.read()
    owner_check_patterns = ["owner_id", "is_superuser", "role == 'owner'"]
    found = sum(1 for p in owner_check_patterns if p in content)
    assert found >= 2, "Organization delete/member remove should check owner role"

def test_member_remove_requires_owner():
    with open("app/routers/organizations.py") as f:
        content = f.read()
    delete_func_start = content.find("def remove_member")
    if delete_func_start == -1:
        delete_func_start = content.find("def delete_org")
    delete_func = content[delete_func_start:delete_func_start + 800]
    assert "owner" in delete_func.lower(), "Member removal should verify owner privileges"
