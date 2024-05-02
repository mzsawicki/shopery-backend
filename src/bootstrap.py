from src.common.s3 import get_local_s3_gateway, bucket_policy_read_public, ObjectStorageGateway

S3_BUCKETS = "product-images", "brand-logos"


def bootstrap_s3_buckets(s3: ObjectStorageGateway = get_local_s3_gateway()) -> None:
    for bucket in S3_BUCKETS:
        bucket_exists = s3.does_bucket_exist(bucket)
        if not bucket_exists:
            s3.create_bucket(bucket)
            s3.set_bucket_policy(bucket, bucket_policy_read_public(bucket))


if __name__ == "__main__":
    bootstrap_s3_buckets()
