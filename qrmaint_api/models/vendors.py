"""Pydantic models for the Vendors domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class Vendor(_CamelModel):
    """A supplier or service vendor in QrMaint.

    Vendors can be referenced in purchase requests and part records to
    indicate where parts are sourced from.

    Attributes:
        id: Internal integer identifier.
        name: Human-readable vendor name.
        external_id: Caller-supplied external identifier.
        description: Optional free-text notes about the vendor.
        active: Whether the vendor is currently selectable.
        created_at: UTC timestamp of record creation.
    """

    id: int
    name: str
    external_id: str | None = None
    description: str | None = None
    active: bool | None = None
    created_at: datetime | None = None


class VendorParams(_CamelModel):
    """Request body for creating a new vendor (POST /vendors).

    Attributes:
        name: Required vendor name.
        external_id: Optional external identifier.
        description: Optional free-text description.
    """

    name: str
    external_id: str | None = None
    description: str | None = None


class UpdatedVendorParams(_CamelModel):
    """Request body for partially updating a vendor (PATCH /vendors/{vendorId}).

    All fields are optional; only provided fields are updated.

    Attributes:
        name: New vendor name.
        external_id: New external identifier (use ``null`` to clear).
        description: New description.
        active: New active state.
    """

    name: str | None = None
    external_id: str | None = None
    description: str | None = None
    active: bool | None = None
