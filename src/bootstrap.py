import asyncio

from redis import Redis, ResponseError
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from src.common.config import Config
from src.common.s3 import (ObjectStorageGateway, bucket_policy_read_public,
                           get_local_s3_gateway)
from src.store.model import product as product_schema

S3_BUCKETS = "product-images", "brand-logos"


def bootstrap_s3_buckets(s3: ObjectStorageGateway = get_local_s3_gateway()) -> None:
    for bucket in S3_BUCKETS:
        bucket_exists = s3.does_bucket_exist(bucket)
        if not bucket_exists:
            s3.create_bucket(bucket)
            s3.set_bucket_policy(bucket, bucket_policy_read_public(bucket))


def bootstrap_redis_indexes(config: Config = Config()) -> None:
    client = Redis(host=config.redis_database_host, port=config.redis_database_port)
    rs = client.ft("idx:products")
    try:
        rs.info()
    except ResponseError:
        rs.create_index(
            product_schema,
            definition=IndexDefinition(prefix=["product:"], index_type=IndexType.JSON),
        )


if __name__ == "__main__":
    bootstrap_s3_buckets()
    bootstrap_redis_indexes()
