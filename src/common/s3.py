import abc
import json
import logging
import typing
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError

from src.common.config import Config


@dataclass(frozen=True, init=True)
class UploadResult:
    success: bool
    file_format_valid: bool = True
    file_size_ok: bool = True
    uploaded_file_path: typing.Optional[str] = None


class ObjectStorageGateway(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def upload_file(
        self, bucket: str, file_key: str, file: typing.BinaryIO
    ) -> UploadResult:
        pass


def bucket_policy_read_public(bucket: str) -> typing.Dict[str, typing.Any]:
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AddPerm",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": f"arn:aws:s3:::{bucket}/*",
            }
        ],
    }


class S3Gateway(ObjectStorageGateway):
    def __init__(self, **kwargs):
        self._emulated_url = kwargs.pop("emulated_url", kwargs.get("endpoint_url"))
        self._client = boto3.client("s3", **kwargs)

    def upload_file(
        self, bucket: str, file_key: str, file: typing.BinaryIO
    ) -> UploadResult:
        try:
            self._client.upload_fileobj(file, bucket, file_key)
            return UploadResult(
                success=True,
                uploaded_file_path=f"{self._emulated_url}/{bucket}/{file_key}",
            )
        except ClientError as error:
            logging.error(error)
            return UploadResult(success=False)

    def create_bucket(self, bucket: str) -> None:
        self._client.create_bucket(Bucket=bucket)

    def set_bucket_policy(
        self, bucket: str, policy: typing.Dict[str, typing.Any]
    ) -> None:
        self._client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))

    def does_bucket_exist(self, bucket: str) -> bool:
        response = self._client.head_bucket(Bucket=bucket)
        return response["ResponseMetadata"]["HTTPStatusCode"] == 200


def get_local_s3_gateway() -> S3Gateway:
    config = Config()
    return S3Gateway(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.s3_region,
        endpoint_url=config.s3_url,
        emulated_url=config.emulated_s3_url,
    )
