import subprocess


def run_build_command(cmd: str):
    subprocess.run(cmd, shell=True)
