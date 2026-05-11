"""Pydantic models for the Parts (spare parts / inventory items) domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class Part(_CamelModel):
    """A spare part or consumable item tracked in QrMaint inventory.

    Attributes:
        id: Internal integer identifier.
        name: Human-readable part name.
        external_id: Caller-supplied external identifier.
        description: Free-text description.
        quantity: Current stock quantity.
        unit: Unit of measurement (e.g. ``"pcs"``, ``"kg"``).
        min_quantity: Minimum stock alert threshold.
        location_id: ID of the storage location.
        location_name: Display name of the storage location.
        category: Part category label.
        created_at: UTC timestamp of record creation.
        updated_at: UTC timestamp of the last modification.
    """

    id: int
    name: str
    external_id: str | None = None
    description: str | None = None
    quantity: float | None = None
    unit: str | None = None
    min_quantity: float | None = None
    location_id: int | None = None
    location_name: str | None = None
    category: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PartParams(_CamelModel):
    """Request body for creating a new part (POST /parts).

    Attributes:
        name: Required part name.
        external_id: Optional external identifier.
        description: Optional free-text description.
        quantity: Optional initial stock quantity.
        unit: Optional unit of measurement.
        min_quantity: Optional minimum stock threshold.
        location_id: Optional storage location ID.
        category: Optional category label.
    """

    name: str
    external_id: str | None = None
    description: str | None = None
    quantity: float | None = None
    unit: str | None = None
    min_quantity: float | None = None
    location_id: int | None = None
    category: str | None = None
