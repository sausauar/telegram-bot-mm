from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - local bootstrap fallback
    def load_dotenv(*_args: object, **_kwargs: object) -> bool:
        return False


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "app" / "resources" / "company_knowledge.md"


def _optional(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _int_env(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if not raw_value:
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if not raw_value:
        return default
    try:
        return float(raw_value)
    except ValueError:
        return default


@dataclass(frozen=True, slots=True)
class Settings:
    app_env: str
    log_level: str
    telegram_bot_token: str | None
    telegram_webhook_secret: str | None
    ai_provider: str
    openai_api_key: str | None
    openai_model: str
    openai_base_url: str | None
    amvera_api_token: str | None
    amvera_api_url: str
    amvera_model: str
    knowledge_base_path: Path
    retrieval_top_k: int
    retrieval_min_score: float
    max_history_messages: int

    @property
    def resolved_ai_provider(self) -> str:
        provider = self.ai_provider.lower().strip()
        if provider != "auto":
            return provider
        if self.amvera_api_token:
            return "amvera"
        if self.openai_api_key:
            return "openai"
        return "offline"

    @property
    def resolved_model(self) -> str:
        if self.resolved_ai_provider == "amvera":
            return self.amvera_model
        return self.openai_model

    @property
    def has_llm_provider(self) -> bool:
        return self.resolved_ai_provider in {"openai", "amvera"}


def load_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env")

    knowledge_base_path = Path(
        os.getenv("KNOWLEDGE_BASE_PATH", str(DEFAULT_KNOWLEDGE_BASE_PATH))
    )
    if not knowledge_base_path.is_absolute():
        knowledge_base_path = PROJECT_ROOT / knowledge_base_path

    return Settings(
        app_env=os.getenv("APP_ENV", "local"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        telegram_bot_token=_optional(os.getenv("TELEGRAM_BOT_TOKEN")),
        telegram_webhook_secret=_optional(os.getenv("TELEGRAM_WEBHOOK_SECRET")),
        ai_provider=os.getenv("AI_PROVIDER", "openai"),
        openai_api_key=_optional(os.getenv("OPENAI_API_KEY")),
        openai_model=os.getenv("OPENAI_MODEL", "gemini-2.5-flash-lite"),
        openai_base_url=_optional(os.getenv("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")),
        amvera_api_token=_optional(os.getenv("AMVERA_API_TOKEN")),
        amvera_api_url=os.getenv(
            "AMVERA_API_URL", "https://kong-proxy.yc.amvera.ru/api/v1/models/gpt"
        ),
        amvera_model=os.getenv("AMVERA_MODEL", "gpt-5"),
        knowledge_base_path=knowledge_base_path,
        retrieval_top_k=_int_env("RETRIEVAL_TOP_K", 5),
        retrieval_min_score=_float_env("RETRIEVAL_MIN_SCORE", 0.12),
        max_history_messages=_int_env("MAX_HISTORY_MESSAGES", 8),
    )
