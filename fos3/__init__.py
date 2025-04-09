from .__about__ import __version__
from .constants import (
    BOTO3_S3_SERVICE_NAME,
    DEFAULT_COMPRESSION,
    DEFAULT_ENCODING,
)
from .hetzner import HetznerS3Bucket, HetznerS3ClientPool
from .s3 import S3Bucket, S3BucketParameters, S3ClientPool

__all__ = (
    # Metadata
    "__version__",
    # Constants
    "BOTO3_S3_SERVICE_NAME",
    "DEFAULT_COMPRESSION",
    "DEFAULT_ENCODING",
    # Hetzner
    # -----
    "HetznerS3Bucket",
    "HetznerS3ClientPool",
    # S3
    # -----
    "S3BucketParameters",
    "S3Bucket",
    "S3ClientPool",
)
