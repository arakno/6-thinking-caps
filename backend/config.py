"""Configuration module for the application."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Provider Selection
    llm_provider: str = "gemini"  # Options: "gemini", "lmstudio"

    # Google Gemini API
    google_api_key: str = ""
    # Use v1beta-supported fully qualified model name (lighter tier)
    gemini_model: str = "models/gemini-flash-lite-latest"

    # LM Studio Configuration
    lmstudio_base_url: str = "http://127.0.0.1:1234"
    lmstudio_model: str = "ibm/granite-4-h-tiny"

    # App
    app_name: str = "6 Thinking Hats Multi-Agent System"
    debug: bool = True
    environment: str = "development"

    # Session management
    session_ttl_minutes: int = 60
    max_concurrent_agents: int = 1

    # API
    api_prefix: str = "/api"

    class Config:
        env_file = str(Path(__file__).parent / ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = False


settings = Settings()
