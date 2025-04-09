import base64
import hashlib
from typing import Optional

import boto3


class S3BucketParameters:
    """
    Configuration class for S3 bucket.
    """

    __slots__ = ("host", "key", "secret", "region")

    def __init__(self, host: str, key: str, secret: str, region: str):
        self.host = host
        self.key = key
        self.secret = secret
        self.region = region

    def __repr__(self) -> str:
        return f"S3BucketParameters(host={self.host})"


class S3ClientPool:
    """
    Manages a pool of S3 clients using boto3 Session for efficient resource management.
    """

    def __init__(self, configuration: S3BucketParameters):
        self._configuration = configuration
        self._session = boto3.Session(
            aws_access_key_id=self._configuration.key,
            aws_secret_access_key=self._configuration.secret,
        )

    def get_client(self) -> boto3.client:
        """
        Returns a configured S3 client.
        """
        return self._session.client(
            "s3",
            region_name=self._configuration.region,
            endpoint_url=self._configuration.host,
        )


class S3Bucket:
    """
    Provides methods to interact with a S3 bucket.
    """

    def __init__(self, bucket_name: str, client_pool: S3ClientPool):
        self._bucket_name = bucket_name
        self._client_pool = client_pool

    def get_object(self, key: str) -> Optional[bytes]:
        """
        Retrieves an object from the S3 bucket.

        :param key: The key (path) of the object in the bucket.
        :return: The content of the object as bytes, or None if the object does not exist.
        """
        if not key:
            raise ValueError("Key cannot be empty.")

        client = self._client_pool.get_client()
        response = client.get_object(Bucket=self._bucket_name, Key=key)
        return response["Body"].read()

    def put_object(self, key: str, data: bytes) -> None:
        """
        Uploads an object to the S3 bucket.

        :param key: The key (path) of the object in the bucket.
        :param data: The content to upload, as bytes.
        """
        if not key:
            raise ValueError("Key cannot be empty.")
        if not data:
            raise ValueError("Data cannot be empty.")

        client = self._client_pool.get_client()
        client.put_object(
            Bucket=self._bucket_name,
            Key=key,
            Body=data,
            ChecksumSHA256=self._calculate_sha256(data),
        )

    def delete_object(self, key: str) -> None:
        """
        Deletes an object from the S3 bucket.

        :param key: The key (path) of the object in the bucket.
        """
        if not key:
            raise ValueError("Key cannot be empty.")

        client = self._client_pool.get_client()
        client.delete_object(Bucket=self._bucket_name, Key=key)

    @staticmethod
    def _calculate_md5(data: bytes) -> str:
        """
        Calculates the MD5 checksum of the data.

        :param data: The data to calculate the checksum for.
        :return: The MD5 checksum as a base64-encoded string.
        """
        return base64.b64encode(hashlib.md5(data).digest()).decode("utf-8")

    @staticmethod
    def _calculate_sha256(data: bytes) -> str:
        """
        Calculates the SHA256 checksum of the data.

        :param data: The data to calculate the checksum for.
        :return: The SHA256 checksum as a hexadecimal string.
        """
        return hashlib.sha256(data).hexdigest()
