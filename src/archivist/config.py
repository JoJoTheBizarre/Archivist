from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """app-wide configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str | None = None

    # embedding model (fastembed)
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dim: int = 384

    # chunking
    chunk_size: int = 512
    chunk_overlap: int = 64

    # server
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
