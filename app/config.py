from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    postgres_dsn: str = os.getenv("POSTGRES_DSN", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")

    amo_domain: str = os.getenv("AMO_DOMAIN", "alkuat")
    amo_token: str = os.getenv("AMO_TOKEN", "")
    custom_field_id: int = int(os.getenv("CUSTOM_FIELD_ID", "886012"))

    stage_2_4_id: int = int(os.getenv("STAGE_2_4_ID", "73295822"))
    stage_6_9_id: int = int(os.getenv("STAGE_6_9_ID", "73295826"))
    stage_12_plus_id: int = int(os.getenv("STAGE_12_PLUS_ID", "73295954"))

    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")


settings = Settings()
