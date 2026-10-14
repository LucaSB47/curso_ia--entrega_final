from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str = "intelligence-hardware-support"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()