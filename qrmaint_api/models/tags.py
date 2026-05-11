"""Pydantic models for the Tags domain."""
from __future__ import annotations

from enum import Enum

from .common import _CamelModel


class TagType(str, Enum):
    """The category of resource a tag is associated with.

    Attributes:
        ASSET: Tag is linked to an asset.
        PRODUCTION_LINE: Tag is linked to a production line.
        WORK_ORDER: Tag is linked to a work order.
    """

    ASSET = "ASSET"
    PRODUCTION_LINE = "PRODUCTION_LINE"
    WORK_ORDER = "WORK_ORDER"


class Tag(_CamelModel):
    """A label that can be attached to QrMaint resources for grouping or filtering.

    Tags provide a free-form classification layer on top of the structured
    hierarchy (assets, locations, etc.).

    Attributes:
        id: Internal integer identifier.
        name: Human-readable tag label.
        type: Resource category this tag applies to (see :class:`TagType`).
        color: Optional hex or named colour used for UI display.
    """

    id: int
    name: str
    type: str | None = None
    color: str | None = None
