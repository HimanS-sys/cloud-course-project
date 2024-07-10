""" Fixture containing set up and tear down for aws testing."""

import os

import boto3
import botocore
import pytest
from moto import mock_aws

from tests.consts import TEST_BUCKET_NAME


def point_away_from_aws():
    os.environ[" AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def mocked_aws():
    with mock_aws():
        # make sure we are not interacting with aws
        point_away_from_aws()

        # create an s3 bucket
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=TEST_BUCKET_NAME)

        yield

        # delete all the objects and the bucket itself
        try:
            response = s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
            for obj in response.get("Contents", []):
                s3_client.delete_object(Bucket=TEST_BUCKET_NAME, Key=obj["Key"])
            s3_client.delete_bucket(Bucket=TEST_BUCKET_NAME)
        except botocore.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchBucket":
                pass
            else:
                raise
