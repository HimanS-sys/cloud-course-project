"""Unit tests for testing the functions in write_objects module."""

import boto3

from files_api.s3.write_objects import upload_s3_object
from tests.consts import TEST_BUCKET_NAME


# pylint: disable=unused-argument
def test__upload_s3_object(mocked_aws: None):
    # upload a file to the bucket with a particular content type
    object_key = "text.txt"
    file_content = b"Hello, World!"
    content_type = "text/plain"
    upload_s3_object(
        bucket_name=TEST_BUCKET_NAME,
        object_key=object_key,
        file_content=file_content,
        content_type=content_type,
    )

    # check that the file was uploaded with a particular content type
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=TEST_BUCKET_NAME, Key=object_key)
    assert response["ContentType"] == content_type
    assert response["Body"].read() == file_content
