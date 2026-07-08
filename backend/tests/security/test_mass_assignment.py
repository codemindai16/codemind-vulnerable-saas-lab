def test_billing_update_has_strict_schema():
    with open("app/routers/billing.py") as f:
        content = f.read()

    dangerous_patterns = [
        "**",
        ".dict()",
        "exclude_unset",
    ]

    use_exclude_unset = "exclude_unset=True" in content
    has_dict_call = ".dict()" in content or ".model_dump()" in content

    assert has_dict_call and use_exclude_unset, \
        "Billing update should use strict schema filtering (exclude_unset=True)"

def test_protected_fields_not_mass_assignable():
    with open("app/schemas/__init__.py") as f:
        content = f.read()

    class_start = content.find("class BillingUpdate")
    class_end = content.find("class Config", class_start) if "class Config" in content[class_start:] else len(content)
    billing_update_class = content[class_start:class_end]

    protected_fields = ["total_spent", "price_per_unit"]
    for field in protected_fields:
        assert field not in billing_update_class, \
            f"Protected field '{field}' should not be in BillingUpdate schema"
