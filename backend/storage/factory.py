from backend.core.config import settings
from backend.storage.local_storage import LocalStorageProvider

def get_storage_provider():
    if settings.STORAGE_PROVIDER == "local":
        return LocalStorageProvider()
    # In the future, we can add S3StorageProvider here
    return LocalStorageProvider()
