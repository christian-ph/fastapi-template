import configparser
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, get_type_hints

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 5432
    DB_NAME: str = "test_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_SCHEMA: str = "public"
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
    APP_NAME: str = "Empty APP"
    LOG_LEVEL: str = "INFO"
    LOG_NAME: str = "Empty App"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["*"]
    ENVIRONMENT: str = "TEST"
    DATABASE: DatabaseSettings | None = None  # Initialized dynamically later
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "fallback_secret_key"))

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @classmethod
    def load_configs(cls):
        config = configparser.ConfigParser()
        config_dir = Path(__file__).parent.parent.parent / "config"
        for file in os.listdir(config_dir):
            if re.match(r".*\.conf$", file):
                config.read(config_dir / file)

        def parse_conf_section(
            model_cls: type[BaseSettings],
            conf_section: dict[str, Any],
        ) -> dict[str, Any]:
            parsed: dict[str, Any] = {}
            model_types = get_type_hints(model_cls)
            for k, raw_value in conf_section.items():
                field = k.upper()
                if field not in model_cls.model_fields:
                    continue

                value = str(raw_value) if raw_value is not None else ""

                try:
                    field_type = model_types.get(field, str)
                    if field_type is bool:
                        parsed[field] = value.lower() in ("true", "1", "t", "yes")
                    elif field_type == list[str]:
                        parsed[field] = [x.strip() for x in value.split(",") if x.strip()]
                    elif field_type is int:
                        parsed[field] = int(value)
                    else:
                        parsed[field] = value
                except Exception as e:
                    print(f"Error parsing field {field}: {e}")
            return parsed

        def merge_env_with_conf(
            model_cls: type[BaseSettings],
            conf_section: dict[str, str],
        ) -> BaseSettings:
            # Load values from .env
            env_values = model_cls().model_dump()

            # Parse values from .conf
            conf_values = parse_conf_section(model_cls, conf_section)

            # Merge: .env takes priority; .conf fills missing fields
            combined = {**conf_values, **env_values}

            print(
                "Combined config - ENV: %s | CONF: %s | FINAL: %s",
                env_values,
                conf_values,
                combined,
            )
            return model_cls(**combined)

        load_dotenv()

        # Main settings (DEFAULT section)
        settings = merge_env_with_conf(cls, config.defaults())

        # Database configuration
        db_section = {}
        if "POSTGRESQL" in config:
            db_section = dict(config["POSTGRESQL"].items())

        print("Loading database configuration: %s", db_section)

        db_kwargs = merge_env_with_conf(DatabaseSettings, db_section)

        settings.DATABASE = DatabaseSettings(**db_kwargs.model_dump())

        return settings


@lru_cache
def get_settings():
    return Settings.load_configs()
