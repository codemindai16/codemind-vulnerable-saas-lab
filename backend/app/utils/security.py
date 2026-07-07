import logging
from app.config import settings

logger = logging.getLogger("codemind")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_security_event(event: str, **kwargs):
    user = kwargs.get("user", "anonymous")
    api_key = kwargs.get("api_key")
    token = kwargs.get("token")

    log_msg = f"SECURITY: {event} | user={user}"
    if api_key:
        log_msg += f" | api_key={api_key}"
    if token:
        log_msg += f" | token={token}"
    for k, v in kwargs.items():
        if k not in ("user", "api_key", "token"):
            log_msg += f" | {k}={v}"

    logger.info(log_msg)
