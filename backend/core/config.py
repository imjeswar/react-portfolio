from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Knowledge Assistant"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "replace_this_with_a_very_secure_secret_key_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    LLM_PROVIDER: str = "openrouter"
    EMBEDDING_PROVIDER: str = "local"
    VECTOR_STORE_PROVIDER: str = "chromadb"
    VECTOR_DB: str = "chromadb"
    STORAGE_PROVIDER: str = "local"
    
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "meta-llama/llama-3.1-8b-instruct"
    OPENROUTER_FALLBACK_MODEL: str = "qwen/qwen-2.5-7b-instruct"
    
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    UPLOAD_DIR: str = "./uploads"
    VECTOR_DB_DIR: str = "./chroma_db"
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
