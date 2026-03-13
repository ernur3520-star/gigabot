from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Credentials / API keys
    green_api_instance: str | None = Field(None, env="GREEN_API_INSTANCE")
    green_api_token: str | None = Field(None, env="GREEN_API_TOKEN")

    telegram_bot_token: str | None = Field(None, env="TELEGRAM_BOT_TOKEN")
    gemini_api_key: str | None = Field(None, env="GEMINI_API_KEY")

    supabase_url: str | None = Field(None, env="SUPABASE_URL")
    supabase_key: str | None = Field(None, env="SUPABASE_KEY")

    # Billing / subscription
    subscription_card: str | None = Field(None, env="SUBSCRIPTION_CARD")
    subscription_price: int = Field(500, env="SUBSCRIPTION_PRICE")
    trial_days: int = Field(7, env="TRIAL_DAYS")

    telegram_seller_id: int | None = Field(None, env="TELEGRAM_SELLER_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
