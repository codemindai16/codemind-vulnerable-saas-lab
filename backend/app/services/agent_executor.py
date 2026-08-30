import subprocess
from typing import Optional

ALLOWED_COMMANDS = {
    "ls", "cat", "echo", "pwd", "whoami", "date", "uname", "df", "ps",
}

class AgentExecutor:
    def execute_command(self, command: str, args: Optional[list[str]] = None) -> dict:
        if command not in ALLOWED_COMMANDS:
            raise ValueError(f"Command '{command}' is not in the allowlist")

        cmd = [command]
        if args:
            cmd.extend(args)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    def execute_safe(self, command: str, args: list[str]) -> dict:
        if command not in ALLOWED_COMMANDS:
            raise ValueError(f"Command '{command}' is not in the allowlist")
        full_command = [command] + args
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    def execute_script(self, script: str) -> dict:
        proc = subprocess.Popen(
            script,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate(timeout=30)
        return {
            "stdout": out.decode(),
            "stderr": err.decode(),
            "return_code": proc.returncode,
        }
