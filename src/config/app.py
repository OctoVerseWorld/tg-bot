from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix='APP_',
        extra="ignore",
    )

    ENVIRONMENT: str
    URL: str


app_settings = Settings()
