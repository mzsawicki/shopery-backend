import logging
import typing
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError

from src.common.config import Config


@dataclass(frozen=True, init=True)
class UploadResult:
    success: bool
    uploaded_file_path: typing.Optional[str] = None


class S3Gateway:
    def __init__(self, **kwargs):
        self._url = kwargs.get("endpoint_url")
        self._client = boto3.client("s3", **kwargs)

    def upload_file(
        self, bucket: str, file_key: str, file: typing.BinaryIO
    ) -> UploadResult:
        try:
            self._client.upload_fileobj(file, bucket, file_key)
            return UploadResult(
                success=True, uploaded_file_path=f"{self._url}/{bucket}/{file_key}"
            )
        except ClientError as error:
            logging.error(error)
            return UploadResult(success=False)


def get_local_s3_gateway() -> S3Gateway:
    config = Config()
    return S3Gateway(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.s3_region,
        endpoint_url=config.s3_url,
    )
