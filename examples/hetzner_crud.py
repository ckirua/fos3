import asyncio
import os

from dotenv import load_dotenv
from fos3.hetzner import HetznerS3Bucket, HetznerS3ClientPool
from fos3.s3 import S3BucketParameters

load_dotenv("/root/workspace/.env", override=True)


def create_configuration() -> S3BucketParameters:
    return S3BucketParameters(
        host=(lambda: os.getenv("OBJECT_STORAGE_HOST"))(),
        key=(lambda: os.getenv("OBJECT_STORAGE_KEY"))(),
        secret=(lambda: os.getenv("OBJECT_STORAGE_SECRET"))(),
    )


def create_pool(
    configuration: S3BucketParameters,
) -> HetznerS3ClientPool:
    return HetznerS3ClientPool(configuration)


def create_bucket(pool: HetznerS3ClientPool) -> HetznerS3Bucket:
    return HetznerS3Bucket(bucket_name="test", client_pool=pool)


def create_file(bucket: HetznerS3Bucket):
    bucket.put_object(key="test.txt", data=b"Hello, world!")


def read_file(bucket: HetznerS3Bucket):
    return bucket.get_object(key="test.txt")


def update_file(bucket: HetznerS3Bucket):
    raise NotImplementedError("Not implemented")


def delete_file(bucket: HetznerS3Bucket):
    return bucket.delete_object(key="test.txt")


async def run_example():
    configuration = create_configuration()
    pool = create_pool(configuration)
    bucket = create_bucket(pool)

    # Create a file
    print("Creating file...")
    create_file(bucket)

    # Read the file
    print("Reading file...")
    file_content = read_file(bucket)
    print(f"File content: {file_content}")

    # Delete the file
    print("Deleting file...")
    delete_file(bucket)


if __name__ == "__main__":
    asyncio.run(run_example())
