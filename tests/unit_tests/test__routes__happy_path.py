"""Module to do unit test on 'main.py'."""

from fastapi import status
from fastapi.testclient import TestClient

# Constants for testing
TEST_FILE_PATH = "test.txt"
TEST_FILE_CONTENT = b"Hello, world!"
TEST_FILE_CONTENT_TYPE = "text/plain"


def test_upload_file(client: TestClient):
    """Test the upload on main.py."""
    # create a file
    test_file_path = "some/nested/file.txt"
    test_file_content = b"some content"
    test_file_content_type = "text/plain"

    response = client.put(
        f"/files/{test_file_path}",
        files={
            "file": (test_file_path, test_file_content, test_file_content_type),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "file_path": test_file_path,
        "message": f"New file uploaded at /{test_file_path}",
    }

    # update an existing file
    updated_content = b"updated content"
    response = client.put(
        f"/files/{test_file_path}",
        files={
            "file": (test_file_path, updated_content, test_file_content_type),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "file_path": test_file_path,
        "message": f"Existing file updated at /{test_file_path}",
    }


def test_list_files_with_pagination(client: TestClient):
    """Test the listing of files with pagination in main.py."""
    for i in range(13):
        client.put(f"/files/file{i}.txt", files={"file": (f"file{i}.txt", TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)})
    response = client.get("/files?page_size=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["files"]) == 10
    assert "next_page_token" in data


def test_get_file_metadata(client: TestClient):
    """Test the fetching of file metadata on main.py."""
    client.put(f"/files/{TEST_FILE_PATH}", files={"file": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)})

    response = client.head(f"/files/{TEST_FILE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    headers = response.headers
    assert headers["Content-Type"] == TEST_FILE_CONTENT_TYPE
    assert headers["Content-Length"] == str(len(TEST_FILE_CONTENT))
    assert "Last-Modified" in headers


def test_get_file(client: TestClient):
    """Test thefetch file on main.py."""
    client.put(f"/files/{TEST_FILE_PATH}", files={"file": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)})

    response = client.get(f"/files/{TEST_FILE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert response.content == TEST_FILE_CONTENT


def test_delete_file(client: TestClient):
    """Test the delete file on main.py."""
    # Upload a file
    client.put(
        f"/files/{TEST_FILE_PATH}",
        files={"file": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )

    # Delete file
    delete_response = client.delete(f"/files/{TEST_FILE_PATH}")
    assert delete_response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/files/{TEST_FILE_PATH}")
    assert get_response.status_code == 404

    # Optionally, try to delete the file again to ensure it returns 404
    second_delete_response = client.delete(f"/files/{TEST_FILE_PATH}")
    assert second_delete_response.status_code == 404
