"""Module to test error handling of the files API."""

import boto3
from fastapi import status
from fastapi.testclient import TestClient

from files_api.schemas import DEFAULT_GET_FILES_MAX_PAGE_SIZE
from tests.consts import TEST_BUCKET_NAME


def test_get_non_exixtant_file(client: TestClient):
    """Test getting non existing file."""
    response = client.get("/v1/files/nonexistantfile.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "File not found"}


def test_head_non_exixtant_file(client: TestClient):
    """Test getting head of non existing file."""
    response = client.head("/v1/files/nonexistantfile.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_non_exixtant_file(client: TestClient):
    """Test deleting non existing file."""
    response = client.delete("/v1/files/nonexistantfile.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "File not found"}


def test_get_files_invaled_page(client: TestClient):
    """Test getting file with invalid page."""
    response = client.get("/v1/files?page_size=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get(f"/v1/files?page_size={DEFAULT_GET_FILES_MAX_PAGE_SIZE + 1}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_validation_mutually_exclusive_parameters(client: TestClient):
    """Test validation of mutually exclusive parameters."""
    # Sending both page_token and directory should raise a 422 error
    response = client.get("/v1/files?page_size=10&page_token=some_token&directory=not_default")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "errors" in response.json()
    assert response.json()["errors"] == [
        "Value error, 'page_token' is mutually exclusive with 'page_size' and 'directory'"
    ]


def test_validation_page_size_greater_than_one(client: TestClient):
    """Sending page_size less than or equal to 0 should raise a 422 error."""
    response = client.get("/v1/files?page_size=0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    assert "detail" in response.json()
    assert "page_size" in str(response.json()["detail"])

    response = client.get("/v1/files?page_size=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()
    assert "page_size" in str(response.json()["detail"])


def test_unforseen_500(client: TestClient):
    """Test 500 internal server error."""
    # delete the s3 bucket and all objects inside
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(TEST_BUCKET_NAME)
    bucket.objects.all().delete()
    bucket.delete()

    # make a request to API to a route that interacts with S3 bucket
    response = client.get("/v1/files")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Internal server error"}
