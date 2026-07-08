import requests
from typing import Optional
from app.config import settings

class WebhookExecutor:
    def __init__(self):
        self.timeout = settings.WEBHOOK_TIMEOUT

    def execute(self, url: str, payload: dict, secret: Optional[str] = None) -> dict:
        headers = {"Content-Type": "application/json"}
        if secret:
            headers["X-Webhook-Secret"] = secret

        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return {"status": response.status_code, "body": response.text}

    def execute_with_redirect(self, url: str, payload: dict) -> dict:
        response = requests.post(url, json=payload, timeout=self.timeout, allow_redirects=True)
        return {"status": response.status_code, "body": response.text}
