"""Configuração do app, lida de variáveis de ambiente e do arquivo .env."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM
    llm_provider: Literal["ollama", "anthropic"] = "ollama"
    ollama_url: str = "http://localhost:11434"
    llm_model: str = "qwen3:8b"
    llm_num_ctx: int = 16384
    anthropic_api_key: str = ""

    # Transcrição
    whisper_model: str = "large-v3-turbo"
    whisper_device: Literal["cuda", "cpu"] = "cuda"
    whisper_compute_type: str = "float16"

    # Limites
    max_video_minutes: int = 180
    chunk_words: int = 1000

    # Infra
    database_url: str = "sqlite:///./data/transcriptor.db"
    storage_dir: Path = Path("./data")
    host: str = "127.0.0.1"
    port: int = 8000


@lru_cache
def get_settings() -> Settings:
    return Settings()
