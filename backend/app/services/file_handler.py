import os
import shutil
from fastapi import UploadFile
from app.config import settings

class FileHandler:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file: UploadFile) -> str:
        filepath = os.path.join(self.upload_dir, file.filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return filepath

    def read_file(self, filename: str) -> bytes:
        filepath = os.path.join(self.upload_dir, filename)
        with open(filepath, "rb") as f:
            return f.read()

    def delete_file(self, filename: str) -> bool:
        filepath = os.path.join(self.upload_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
