import subprocess
from typing import Optional
import os
import json

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

    def execute_with_env(self, command: str, args: list[str], env_vars: dict) -> dict:
        if command not in ALLOWED_COMMANDS:
            raise ValueError(f"Command '{command}' is not in the allowlist")
        env = os.environ.copy()
        env.update(env_vars)
        cmd = [command] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    def execute_pipeline(self, commands: list[list[str]]) -> list[dict]:
        results = []
        for cmd in commands:
            if cmd[0] not in ALLOWED_COMMANDS:
                raise ValueError(f"Command '{cmd[0]}' is not in the allowlist")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            results.append({
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            })
        return results

    def get_system_info(self) -> dict:
        return self.execute_command("uname", ["-a"])

    def list_processes(self) -> dict:
        return self.execute_command("ps", ["aux"])

    def check_disk_space(self) -> dict:
        return self.execute_command("df", ["-h"])
