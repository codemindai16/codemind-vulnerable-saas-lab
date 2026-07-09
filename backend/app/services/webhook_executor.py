import ipaddress
import requests
from typing import Optional
from urllib.parse import urlparse
from app.config import settings

BLOCKED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
]

BLOCKED_NETWORKS = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "127.0.0.0/8",
]


class WebhookExecutor:
    def __init__(self):
        self.timeout = settings.WEBHOOK_TIMEOUT

    def _is_internal(self, hostname: str) -> bool:
        if hostname in BLOCKED_HOSTS:
            return True
        try:
            addr = ipaddress.ip_address(hostname)
            for network in BLOCKED_NETWORKS:
                if addr in ipaddress.ip_network(network):
                    return True
        except ValueError:
            pass
        return False

    def execute(self, url: str, payload: dict, secret: Optional[str] = None) -> dict:
        parsed = urlparse(url)
        if self._is_internal(parsed.hostname):
            raise ValueError(f"SSRF blocked: cannot connect to internal host '{parsed.hostname}'")
        if parsed.scheme not in ("https",):
            raise ValueError(f"Only HTTPS URLs allowed, got '{parsed.scheme}'")

        headers = {"Content-Type": "application/json"}
        if secret:
            headers["X-Webhook-Secret"] = secret

        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return {"status": response.status_code, "body": response.text}

    def execute_with_redirect(self, url: str, payload: dict) -> dict:
        parsed = urlparse(url)
        if self._is_internal(parsed.hostname):
            raise ValueError(f"SSRF blocked: cannot connect to internal host '{parsed.hostname}'")
        response = requests.post(url, json=payload, timeout=self.timeout, allow_redirects=True)
        return {"status": response.status_code, "body": response.text}
