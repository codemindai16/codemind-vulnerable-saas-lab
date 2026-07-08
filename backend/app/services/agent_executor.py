import subprocess
from typing import Optional

class AgentExecutor:
    def execute_command(self, command: str) -> dict:
        result = subprocess.run(
            command,
            shell=True,
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
