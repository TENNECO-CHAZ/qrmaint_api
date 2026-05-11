"""Pydantic models for the Dictionaries domain."""

from datetime import datetime

from .common import _CamelModel


class DictionaryRootParent(_CamelModel):
    """The top-level category of a QrMaint dictionary.

    Dictionaries are key-value stores used for configurable dropdowns
    (failure codes, reasons, etc.).  Each root parent groups a set of items.

    Attributes:
        id: Internal integer identifier.
        name: Category name shown in the UI.
        type: Machine-readable type identifier.
        description: Optional description of this dictionary group.
    """

    id: int
    name: str
    type: str | None = None
    description: str | None = None


class DictionaryItem(_CamelModel):
    """A single item within a QrMaint dictionary.

    Attributes:
        id: Internal integer identifier.
        name: Item label shown in dropdowns.
        root_parent_id: ID of the top-level dictionary this item belongs to.
        parent_id: ID of the direct parent item (for nested dictionaries).
        description: Optional description.
        active: Whether the item is currently selectable.
        created_at: UTC timestamp of record creation.
    """

    id: int
    name: str
    root_parent_id: int | None = None
    parent_id: int | None = None
    description: str | None = None
    active: bool | None = None
    created_at: datetime | None = None


class DictionariesItemParams(_CamelModel):
    """Request body for creating a new dictionary item (POST /dictionaries/{rootParentId}/items).

    Attributes:
        name: Required item label.
        parent_id: Optional parent item ID for nested hierarchies.
        description: Optional description.
    """

    name: str
    parent_id: int | None = None
    description: str | None = None


class UpdatedDictionaryItemParams(_CamelModel):
    """Request body for partially updating a dictionary item (PATCH).

    All fields are optional; only provided fields are updated.

    Attributes:
        name: New item label.
        description: New description.
        active: New active state.
    """

    name: str | None = None
    description: str | None = None
    active: bool | None = None
