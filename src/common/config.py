from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Development
    enable_local_aws_emulation: bool
    emulated_s3_url: str = Field()

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

    # AWS S3
    s3_url: str = Field()
    aws_access_key_id: str = Field()
    aws_secret_access_key: str = Field()
    s3_region: str = Field()

    # File upload
    max_upload_file_size_bytes: int = Field()

    # CORS
    cors_origins: str = Field()
