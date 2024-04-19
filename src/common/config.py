from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Dev mode
    dev_mode: bool = Field(default=False)

    # Filesystem
    base_dir: Path = Path(__file__).parent.parent.parent
    project_root: Path = base_dir.parent

    # Database
    postgres_database_name: str = Field()
    postgres_user: str = Field()
    postgres_password: str = Field()
    postgres_host: str = Field()
    postgres_port: int = Field()

    # Redis (streams)
    redis_streams_host: str = Field()
    redis_streams_port: int = Field()

    # Redis (in-memory database)
    redis_database_host: str = Field()
    redis_database_port: int = Field()
