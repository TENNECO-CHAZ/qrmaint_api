"""Shared base classes, generic types, and enumerations used across all models."""

from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class _CamelModel(BaseModel):
    """Base Pydantic model that maps camelCase JSON keys to snake_case attributes.

    All QrMaint API responses use camelCase field names.  This base class
    configures ``alias_generator=to_camel`` so that Python code can use
    conventional snake_case while serialisation/deserialisation handles the
    conversion transparently.

    To serialise for an outgoing request use::

        model.model_dump(by_alias=True, exclude_none=True)
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class IdType(str, Enum):
    """Specifies which identifier type is used when addressing a resource by ID.

    Attributes:
        ID: Use the internal integer ID (default).
        EXTERNAL_ID: Use the caller-supplied external identifier string.
    """

    ID = "ID"
    EXTERNAL_ID = "EXTERNAL_ID"


class DictionaryItemType(str, Enum):
    """Enumerates the built-in dictionary item categories.

    Attributes:
        FAILURE_CODE: Items that represent failure codes.
        REASON: Items that represent downtime or event reasons.
    """

    FAILURE_CODE = "FAILURE_CODE"
    REASON = "REASON"


class PaginatedResponse(_CamelModel, Generic[T]):
    """Generic wrapper for all paginated list responses from the API.

    Attributes:
        data: The list of items on the current page.
        all_records_count: Total number of records matching the query across
            all pages.
    """

    data: list[T]
    all_records_count: int


class CreatedObject(_CamelModel):
    """Response payload returned after a successful resource creation (HTTP 201).

    Attributes:
        id: The auto-assigned internal ID of the newly created resource.
    """

    id: int


class UpdatedObject(_CamelModel):
    """Response payload returned after a successful resource update (HTTP 200).

    Attributes:
        updated: ``True`` when the resource was modified.
    """

    updated: bool


class EmbeddedTag(_CamelModel):
    """A tag embedded in a resource list/detail response.

    Attributes:
        id: Internal tag identifier.
        name: Tag label.
    """

    id: int
    name: str


class EmbeddedAttachment(_CamelModel):
    """An attachment embedded in a resource list/detail response.

    Attributes:
        id: Internal attachment identifier.
        file_name: Original file name including extension.
        size: File size in bytes.
        type: MIME type (e.g. ``"image/jpeg"``).
        type_group: High-level group (e.g. ``"IMAGE"``, ``"OTHER"``).
        created_datetime: UTC timestamp of upload.
    """

    id: int
    file_name: str | None = None
    size: int | None = None
    type: str | None = None
    type_group: str | None = None
    created_datetime: datetime | None = None
