from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from src.common.config import Config
from src.common.model import Entity


def construct_connection_string(
    user: str,
    password: str,
    host: str,
    port: int,
    database_name: str,
    async_: bool = True,
) -> str:
    driver = "postgresql+asyncpg" if async_ else "postgresql"
    return f"{driver}://{user}:{password}@{host}:{port}/{database_name}"


def connection_string_from_config(config: Config, async_: bool = True) -> str:
    dsn = construct_connection_string(
        config.postgres_user,
        config.postgres_password,
        config.postgres_host,
        config.postgres_port,
        config.postgres_database_name,
        async_=async_,
    )
    return dsn


def create_database_engine(connection_string: str) -> AsyncEngine:
    return create_async_engine(connection_string)


async def drop_all_entities(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Entity.metadata.drop_all)


async def create_all_entities(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Entity.metadata.create_all)


def get_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, class_=AsyncSession)


async def dispose_engine(engine: AsyncEngine) -> None:
    await engine.dispose()


_engine = create_database_engine(connection_string_from_config(Config()))


def get_db() -> async_sessionmaker:
    return get_session_factory(_engine)
