import pyarrow.fs as fs

from ..s3 import S3BucketParameters


def create_s3_filesystem(
    bucket_parameters: S3BucketParameters,
) -> fs.S3FileSystem:
    return fs.S3FileSystem(
        endpoint_override=bucket_parameters.host,
        access_key=bucket_parameters.key,
        secret_key=bucket_parameters.secret,
        region=bucket_parameters.region,
    )
