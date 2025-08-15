"""Carga de configuración central desde variables de entorno (.env)."""
from __future__ import annotations
from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()  # Carga .env si existe

class Settings(BaseModel):
    whisper_api_key: str | None = os.getenv("LLMWHISPERER_API_KEY")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
