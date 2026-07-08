import os
import shutil
from backend.core.interfaces import StorageProvider
from backend.core.config import settings

class LocalStorageProvider(StorageProvider):
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file_bytes: bytes, filename: str) -> str:
        file_path = os.path.join(self.upload_dir, filename)
        
        # Avoid overriding existing files by appending a counter if needed
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(self.upload_dir, f"{base}_{counter}{extension}")
            counter += 1

        with open(file_path, "wb") as f:
            f.write(file_bytes)
        return file_path

    def delete_file(self, file_path: str) -> bool:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def read_file(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()
