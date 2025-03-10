from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix='TELEGRAM_API_',
        extra="ignore",
    )

    TOKEN: str
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str

    ADMIN_IDS: list[int]


tg_api_settings = Settings()
