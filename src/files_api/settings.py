"""Module containing conf of the codebase."""

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Settings for the files API."""

    s3_bucket_name: str = Field(...)

    model_config = SettingsConfigDict(case_sensitive=False)
