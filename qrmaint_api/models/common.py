"""Shared base classes, generic types, and enumerations used across all models."""
from __future__ import annotations

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

    def model_dump(self, *, mode: str = "json", **kwargs):
        return super().model_dump(mode=mode, **kwargs)


class IdType(str, Enum):
    """Specifies which identifier type is used when addressing a resource by ID.

    Attributes:
        ID: Use the internal integer ID (default).
        EXTERNAL_ID: Use the caller-supplied external identifier string.
    """

    ID = "ID"
    EXTERNAL_ID = "EXTERNAL_ID"


class DictionaryItemType(str, Enum):
    """Enumerates the dictionary item parent categories (DICTIONARY_ITEMS_TYPES)."""

    TYPE_OF_WORK = "TYPE_OF_WORK"
    PART_TYPE = "PART_TYPE"
    EQUIPMENT_TYPE = "EQUIPMENT_TYPE"
    EQUIPMENT_STATUS = "EQUIPMENT_STATUS"
    COST_ACCOUNT = "COST_ACCOUNT"
    INVENTORY_DOCUMENT_TYPES = "INVENTORY_DOCUMENT_TYPES"
    MEASUREMENT_UNITS_FOR_READING_AND_MEASUREMENT = "MEASUREMENT_UNITS_FOR_READING_AND_MEASUREMENT"
    LOCATION_TYPE = "LOCATION_TYPE"
    MEASUREMENT_UNITS_FOR_QUANTITY = "MEASUREMENT_UNITS_FOR_QUANTITY"
    MANUFACTURER = "MANUFACTURER"
    WORK_STATUS = "WORK_STATUS"
    TYPE_OF_SERVICE = "TYPE_OF_SERVICE"
    PURCHASE_REQUEST_PURPOSE = "PURCHASE_REQUEST_PURPOSE"
    STOCK_MOVEMENT_TYPES = "STOCK_MOVEMENT_TYPES"
    PURCHASE_REQUEST_STATUS = "PURCHASE_REQUEST_STATUS"
    CRITICALITY = "CRITICALITY"


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
        id: The internal ID of the updated resource.
    """

    id: int


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
