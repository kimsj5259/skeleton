from typing import Any, Optional, Union, ClassVar  # ClassVar 추가
import os

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator, EmailStr, AnyHttpUrl


class Settings(BaseSettings):
    """General"""

    APP_ENV: str
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/{API_VERSION}"
    PROJECT_NAME: str

    """Database"""
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    ASYNC_DATABASE_URI: Optional[PostgresDsn]  # Optional 사용

    @field_validator("ASYNC_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=str(values.get("DATABASE_PORT")),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )

    DB_POOL_SIZE: ClassVar[int] = 83  # ClassVar로 선언
    WEB_CONCURRENCY: ClassVar[int] = 9  # ClassVar로 선언
    POOL_SIZE: ClassVar[int] = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)  # ClassVar로 선언

    """Initial"""
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    """CORS"""
    BACKEND_CORS_ORIGINS: Union[list[str], list[AnyHttpUrl]]  # Union 사용

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings()
