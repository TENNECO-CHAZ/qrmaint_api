"""Pydantic models for the Dictionaries domain."""
from __future__ import annotations

from .common import _CamelModel


class DictionaryRootParent(_CamelModel):
    """A top-level dictionary category in QrMaint."""

    id: int
    name: str | None = None
    is_extendable: bool | None = None


class DictionariesItem(_CamelModel):
    """A single item within a QrMaint dictionary category."""

    id: int
    name: str | None = None
    readonly: bool | None = None
    parent_id: int | None = None
    external_id: str | None = None


class DictionaryItem(_CamelModel):
    """Embedded dictionary reference (id + name) used in work orders and other resources."""

    id: int
    name: str | None = None


class DictionariesItemParams(_CamelModel):
    """Request body for creating or updating a dictionary item."""

    name: str | None = None
    external_id: str | None = None


class UpdatedDictionaryItemParams(_CamelModel):
    """Request body for partially updating a dictionary item (PATCH)."""

    name: str | None = None
    external_id: str | None = None
