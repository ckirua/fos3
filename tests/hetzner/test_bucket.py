import hashlib
import unittest
from unittest.mock import MagicMock, patch

from fos3.hetzner.bucket import (
    HetznerS3Bucket,
    HetznerS3BucketConfiguration,
    HetznerS3ClientPool,
)


class TestHetznerS3BucketConfiguration(unittest.TestCase):
    def test_init(self):
        config = HetznerS3BucketConfiguration(
            host="https://s3.eu-central-1.amazonaws.com",
            key="test_key",
            secret="test_secret",
        )
        self.assertEqual(config.host, "https://s3.eu-central-1.amazonaws.com")
        self.assertEqual(config.key, "test_key")
        self.assertEqual(config.secret, "test_secret")


class TestHetznerS3ClientPool(unittest.TestCase):
    @patch("boto3.Session")
    def test_get_client(self, mock_session):
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client

        config = HetznerS3BucketConfiguration(
            host="https://s3.eu-central-1.amazonaws.com",
            key="test_key",
            secret="test_secret",
        )
        client_pool = HetznerS3ClientPool(config)

        client = client_pool.get_client()

        self.assertEqual(client, mock_client)
        mock_session.assert_called_once_with(
            aws_access_key_id="test_key",
            aws_secret_access_key="test_secret",
        )
        mock_session.return_value.client.assert_called_once_with(
            "s3",
            region_name="fsn1",
            endpoint_url="https://s3.eu-central-1.amazonaws.com",
        )


class TestHetznerS3Bucket(unittest.TestCase):
    def setUp(self):
        self.mock_client_pool = MagicMock()
        self.mock_client = MagicMock()
        self.mock_client_pool.get_client.return_value = self.mock_client
        self.bucket = HetznerS3Bucket("test-bucket", self.mock_client_pool)

    def test_get_object(self):
        mock_body = MagicMock()
        mock_body.read.return_value = b"test data"
        self.mock_client.get_object.return_value = {"Body": mock_body}

        result = self.bucket.get_object("test-key")

        self.assertEqual(result, b"test data")
        self.mock_client.get_object.assert_called_once_with(
            Bucket="test-bucket", Key="test-key"
        )

    def test_get_object_empty_key(self):
        with self.assertRaises(ValueError) as context:
            self.bucket.get_object("")
        self.assertEqual(str(context.exception), "Key cannot be empty.")

    def test_put_object(self):
        data = b"test data"
        self.bucket.put_object("test-key", data)

        self.mock_client.put_object.assert_called_once_with(
            Bucket="test-bucket",
            Key="test-key",
            Body=data,
            ContentMD5=self.bucket._calculate_md5(data),
        )

    def test_put_object_empty_key(self):
        with self.assertRaises(ValueError) as context:
            self.bucket.put_object("", b"test data")
        self.assertEqual(str(context.exception), "Key cannot be empty.")

    def test_put_object_empty_data(self):
        with self.assertRaises(ValueError) as context:
            self.bucket.put_object("test-key", b"")
        self.assertEqual(str(context.exception), "Data cannot be empty.")

    def test_delete_object(self):
        self.bucket.delete_object("test-key")

        self.mock_client.delete_object.assert_called_once_with(
            Bucket="test-bucket", Key="test-key"
        )

    def test_delete_object_empty_key(self):
        with self.assertRaises(ValueError) as context:
            self.bucket.delete_object("")
        self.assertEqual(str(context.exception), "Key cannot be empty.")

    def test_calculate_md5(self):
        data = b"test data"
        # The _calculate_md5 method should return a hexdigest string
        expected_md5 = hashlib.md5(data).hexdigest()

        result = self.bucket._calculate_md5(data)

        self.assertEqual(result, expected_md5)


if __name__ == "__main__":
    unittest.main()
