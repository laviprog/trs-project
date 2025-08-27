from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    BOT_TOKEN: str
    CHANNEL_NAME: str

    ARCHIVE_URL: str
    TOKEN: str

    AI_MODEL: str
    AI_BASE_URL: str
    AI_EMAIL: str
    AI_PASSWORD: str

    TRANSCRIPTION_BASE_URL: str
    TRANSCRIPTION_USERNAME: str
    TRANSCRIPTION_PASSWORD: str


settings = Settings()
