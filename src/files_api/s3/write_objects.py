"""Functions for writing objects from an S3 bucket--the "C" and "U" in CRUD."""

from typing import Optional

import boto3

try:
    from mypy_boto3_s3 import S3Client
except ImportError:
    ...


def upload_s3_object(
    bucket_name: str,
    object_key: str,
    file_content: bytes,
    content_type: Optional[str] = None,
    s3_client: Optional["S3Client"] = None,
) -> None:
    """Upload S3 Object."""
    s3_client = s3_client or boto3.client("s3")
    content_type = content_type or "application/octet-stream"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=file_content,
        ContentType=content_type,
    )
    return
