from src.common.s3 import get_local_s3_gateway, bucket_policy_read_public

S3_BUCKETS = "product-images", "brand-logos"

if __name__ == "__main__":
    s3 = get_local_s3_gateway()
    for bucket in S3_BUCKETS:
        bucket_exists = s3.does_bucket_exist(bucket)
        if not bucket_exists:
            s3.create_bucket(bucket)
            s3.set_bucket_policy(bucket, bucket_policy_read_public(bucket))
