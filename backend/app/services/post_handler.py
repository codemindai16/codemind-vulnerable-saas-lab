import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.config import settings

ALLOWED_MIME_TYPES = {
    "text/plain",
    "text/csv",
    "application/json",
    "application/xml",
    "text/xml",
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/gif",
}


class PostHandler:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.max_size = settings.MAX_UPLOAD_SIZE

    def save_media(self, file: UploadFile) -> str:
        safe_name = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
        safe_path = self.upload_dir / safe_name
        safe_path = safe_path.resolve()

        if not str(safe_path).startswith(str(self.upload_dir.resolve())):
            raise ValueError("Path traversal detected")

        content = file.file.read(self.max_size + 1)
        if len(content) > self.max_size:
            raise ValueError(f"File exceeds maximum size of {self.max_size} bytes")

        with open(safe_path, "wb") as buffer:
            buffer.write(content)

        return str(safe_path)

    def read_media(self, filename: str) -> bytes:
        safe_path = (self.upload_dir / filename).resolve()
        if not str(safe_path).startswith(str(self.upload_dir.resolve())):
            raise ValueError("Path traversal detected")
        with open(safe_path, "rb") as f:
            return f.read()

    def delete_media(self, filename: str) -> bool:
        safe_path = (self.upload_dir / filename).resolve()
        if not str(safe_path).startswith(str(self.upload_dir.resolve())):
            raise ValueError("Path traversal detected")
        if safe_path.exists():
            safe_path.unlink()
            return True
        return False
