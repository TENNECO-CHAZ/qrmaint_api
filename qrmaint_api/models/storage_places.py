"""Pydantic models for the Storage Places domain."""

from .common import _CamelModel


class StoragePlace(_CamelModel):
    """A named storage location within a warehouse.

    Storage places can be nested (aisles, shelves, bins) and are referenced by
    stock records to pinpoint where a part is physically located.

    Attributes:
        id: Internal integer identifier.
        name: Human-readable location name (e.g. ``"Shelf A-3"``).
        external_id: Caller-supplied external identifier.
        path: Full hierarchical path from the warehouse root.
        warehouse_id: ID of the warehouse this location belongs to.
        warehouse_name: Display name of the warehouse.
        parent_id: ID of the parent storage place for nested hierarchies.
    """

    id: int
    name: str
    external_id: str | None = None
    path: str | None = None
    warehouse_id: int | None = None
    warehouse_name: str | None = None
    parent_id: int | None = None


class StoragePlaceParams(_CamelModel):
    """Request body for creating a new storage place (POST /dictionaries/storage-places).

    Attributes:
        name: Required location name.
        warehouse_id: Required ID of the owning warehouse.
        external_id: Optional external identifier.
        parent_id: Optional parent storage place ID for nested hierarchies.
    """

    name: str
    warehouse_id: int
    external_id: str | None = None
    parent_id: int | None = None


class UpdatedStoragePlaceParams(_CamelModel):
    """Request body for partially updating a storage place
    (PATCH /dictionaries/storage-places/{storagePlaceId}).

    All fields are optional; only provided fields are updated.

    Attributes:
        name: New location name.
        external_id: New external identifier (use ``null`` to clear).
        parent_id: New parent storage place ID.
    """

    name: str | None = None
    external_id: str | None = None
    parent_id: int | None = None
