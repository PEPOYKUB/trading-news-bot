from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    app_name: str = "Trading News Intelligence Bot"
    database_url: str = "sqlite:///data/news.db"
    timezone: str = "Asia/Bangkok"
    ai_provider: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    watchlist: str = "EURUSD,GBPUSD,XAUUSD,BTCUSD,NAS100"
    fetch_interval_minutes: int = 5
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    notification_provider: str = "console"
    enable_rss: bool = True

    @property
    def database_path(self) -> Path:
        return BASE_DIR / self.database_url.removeprefix("sqlite:///")

    @property
    def watchlist_items(self) -> list[str]:
        return [x.strip().upper() for x in self.watchlist.split(",") if x.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
