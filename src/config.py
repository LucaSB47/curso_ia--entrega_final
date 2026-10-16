from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "final"
    LANGSMITH_API_KEY: str
    LANGSMITH_TRACING: bool = True
    LANGSMITH_PROJECT: str = "intelligence-hardware-support"
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.8-flash"
    OPENAI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()