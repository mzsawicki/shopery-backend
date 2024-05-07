from redis.asyncio import Redis

from src.common.config import Config


def get_redis_client() -> Redis:
    config = Config()
    return Redis(host=config.redis_database_host, port=config.redis_database_port)
