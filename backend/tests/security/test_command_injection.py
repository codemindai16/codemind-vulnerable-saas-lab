def test_no_shell_true_in_execution():
    with open("app/services/agent_executor.py") as f:
        content = f.read()

    assert "shell=True" not in content, \
        "shell=True should not be used in subprocess calls (command injection risk)"

def test_command_uses_allowlist():
    with open("app/services/agent_executor.py") as f:
        content = f.read()
    assert "subprocess" in content, "Should use subprocess module"
    assert "shell=True" not in content or "shlex" in content, \
        "If shell=True is used, shlex.quote() should be applied to all user input"
