"""Module containing schemas."""

from datetime import datetime
from typing import (
    List,
    Optional,
    Self,
)

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)

####################################
# --- Request/response schemas --- #
####################################

# Constants
DEFAULT_GET_FILES_PAGE_SIZE = 10
DEFAULT_GET_FILES_MIN_PAGE_SIZE = 10
DEFAULT_GET_FILES_MAX_PAGE_SIZE = 100
DEFAULT_GET_FILES_DIRECTORY = ""


# read (cRud)
class FileMetadata(BaseModel):
    """Request schema for Files."""

    file_path: str
    last_modified: datetime
    size_bytes: int


class GetFilesQueryParams(BaseModel):
    """Queryparam"""

    page_size: int = Field(
        DEFAULT_GET_FILES_PAGE_SIZE,
        ge=DEFAULT_GET_FILES_MIN_PAGE_SIZE,
        le=DEFAULT_GET_FILES_MAX_PAGE_SIZE,
    )
    directory: Optional[str] = DEFAULT_GET_FILES_DIRECTORY
    page_token: Optional[str] = None

    @model_validator(mode="after")
    def check_page_token(self) -> Self:
        if self.page_token:
            get_files_query_params: dict = self.model_dump(exclude_unset=True)
            page_size_set = "page_size" in get_files_query_params.keys()
            directory_set = "directory" in get_files_query_params.keys()
            if page_size_set or directory_set:
                raise ValueError("'page_token' is mutually exclusive with 'page_size' and 'directory'")
        return self


class PutFileResponse(BaseModel):
    """Response schema for PUT API."""

    file_path: str
    message: str


class GetFilesResponse(BaseModel):
    """Response schema for get api."""

    files: List[FileMetadata]
    next_page_token: Optional[str]
