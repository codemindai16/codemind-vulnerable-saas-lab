"""Webhook canary smoke file (Faz 5 live verification)."""
import os


def get_env(key: str, default: str = "") -> str:
    return os.getenv(key, default)
