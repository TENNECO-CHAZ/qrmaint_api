"""Pydantic models for the Tags domain."""
from __future__ import annotations

from enum import Enum

from .common import _CamelModel


class TagType(str, Enum):
    """Resource category a tag is associated with."""

    WORK = "WORK"
    EQUIPMENT = "EQUIPMENT"
    VENDOR = "VENDOR"
    PART = "PART"
    PRODUCTION_AREA = "PRODUCTION_AREA"
    ATTACHMENT = "ATTACHMENT"
    PRODUCTION_LINE = "PRODUCTION_LINE"


class Tag(_CamelModel):
    """A label that can be attached to QrMaint resources for grouping or filtering."""

    id: int
    name: str | None = None
    resource_type: TagType | None = None
