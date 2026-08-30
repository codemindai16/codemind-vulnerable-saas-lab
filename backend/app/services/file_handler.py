import os
from pathlib import Path
from typing import Optional

class FileHandler:
    def __init__(self, base_path: str = "/app/data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def write_file(self, path: str, content: str) -> dict:
        safe_path = self._sanitize_path(path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_text(content, encoding="utf-8")
        return {"path": str(safe_path), "bytes_written": len(content.encode("utf-8"))}

    def read_file(self, path: str) -> dict:
        safe_path = self._sanitize_path(path)
        if not safe_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        content = safe_path.read_text(encoding="utf-8")
        return {"path": str(safe_path), "content": content, "size": len(content)}

    def delete_file(self, path: str) -> dict:
        safe_path = self._sanitize_path(path)
        if safe_path.exists():
            safe_path.unlink()
            return {"deleted": True, "path": str(safe_path)}
        return {"deleted": False, "path": str(safe_path)}

    def list_files(self, path: str = "") -> dict:
        safe_path = self._sanitize_path(path)
        if not safe_path.exists():
            return {"files": []}
        files = []
        for item in safe_path.iterdir():
            files.append({
                "name": item.name,
                "path": str(item.relative_to(self.base_path)),
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else None,
            })
        return {"files": files}

    def _sanitize_path(self, path: str) -> Path:
        # Prevent path traversal
        path = path.replace("..", "").lstrip("/\")
        return self.base_path / path

    def append_file(self, path: str, content: str) -> dict:
        safe_path = self._sanitize_path(path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        with safe_path.open("a", encoding="utf-8") as f:
            f.write(content)
        return {"path": str(safe_path), "bytes_appended": len(content.encode("utf-8"))}

    def copy_file(self, src: str, dst: str) -> dict:
        safe_src = self._sanitize_path(src)
        safe_dst = self._sanitize_path(dst)
        safe_dst.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(safe_src, safe_dst)
        return {"source": str(safe_src), "destination": str(safe_dst)}

    def move_file(self, src: str, dst: str) -> dict:
        safe_src = self._sanitize_path(src)
        safe_dst = self._sanitize_path(dst)
        safe_dst.parent.mkdir(parents=True, exist_ok=True)
        safe_src.rename(safe_dst)
        return {"source": str(safe_src), "destination": str(safe_dst)}

    def get_file_info(self, path: str) -> dict:
        safe_path = self._sanitize_path(path)
        if not safe_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        stat = safe_path.stat()
        return {
            "path": str(safe_path),
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_dir": safe_path.is_dir(),
        }
