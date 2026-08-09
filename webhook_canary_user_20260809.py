"""Webhook canary (user push) - Faz 5 live verification. Author: codemindai16 (user identity)."""
import os

def resolve(key: str, default: str = "") -> str:
    return os.getenv(key, default)

def canary() -> str:
    return resolve("CANARY", "ok")
