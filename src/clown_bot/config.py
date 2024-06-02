"""Configuration for ClownBot"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Config class for ClownBot

    Attributes:
        discord_token: SecretStr: The bot's Discord token
        db_connection_str: SecretStr: The bot's database connection string
        prefix: str: The bot's command prefix
    """

    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", extra="ignore"
    )

    discord_token: SecretStr
    db_connection_str: SecretStr
    prefix: str = "!"
    admin_ids: list[int] = [
        114384475743453193,  # Nick
        114338477922975745,  # Lucas
    ]
    log_level: str = "INFO"
    name_cache_ttl_seconds: int = 600
