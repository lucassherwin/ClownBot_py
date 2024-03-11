"""Configuration for ClownBot"""
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Config class for ClownBot
    
    Attributes:
        discord_token: SecretStr: The bot's Discord token
        prefix: str: The bot's command prefix
    """
    model_config = SettingsConfigDict(case_sensitive=False,
                                      env_file=".env",
                                      extra="ignore")

    discord_token: SecretStr
    prefix: str = "!"
