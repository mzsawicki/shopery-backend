from src.common.s3 import get_local_s3_gateway

if __name__ == "__main__":
    s3 = get_local_s3_gateway()
    s3_buckets = "product-images", "brand-logos"
    for bucket in s3_buckets:
        s3.create_bucket(bucket)
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::{bucket}/*'
            }]
        }
        s3.set_bucket_policy(bucket, bucket_policy)

