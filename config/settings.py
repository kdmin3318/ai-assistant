"""Pydantic Settings - .env 기반 설정 관리."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    llm_provider: str = "claude"
    llm_model: str = "claude-sonnet-4-6"

    # API Keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    # Google Calendar
    google_credentials_path: Path = Path("credentials.json")
    google_token_path: Path = Path("token.json")
    google_calendar_id: str = "primary"

    # App
    timezone: str = "Asia/Seoul"

    def get_litellm_model(self) -> str:
        """LLM provider에 맞는 litellm 모델 문자열 반환."""
        provider_map = {
            "claude": f"anthropic/{self.llm_model}",
            "openai": self.llm_model,
            "ollama": f"ollama/{self.llm_model}",
        }
        return provider_map.get(self.llm_provider, self.llm_model)


settings = Settings()
