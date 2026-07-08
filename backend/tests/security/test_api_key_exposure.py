def test_api_key_not_in_user_response():
    with open("app/schemas/__init__.py") as f:
        content = f.read()

    class_start = content.find("class UserOut")
    class_end = content.find("class Config", class_start)
    user_out_class = content[class_start:class_end]

    assert "api_key" not in user_out_class, "api_key should not be in UserOut response schema"
