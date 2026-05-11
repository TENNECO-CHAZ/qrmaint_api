"""Pydantic models for the Purchase Requests domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class PurchaseRequestItem(_CamelModel):
    """A single line item within a purchase request.

    Attributes:
        id: Internal integer identifier.
        part_id: ID of the requested part.
        part_name: Display name of the part.
        quantity: Requested quantity.
        unit: Unit of measurement.
        price: Unit price.
        supplier_id: ID of the preferred supplier.
        supplier_name: Display name of the supplier.
        asset_id: ID of the asset this part is destined for.
        asset_name: Display name of the asset.
        description: Additional notes for this line.
    """

    id: int | None = None
    part_id: int | None = None
    part_name: str | None = None
    quantity: float | None = None
    unit: str | None = None
    price: float | None = None
    supplier_id: int | None = None
    supplier_name: str | None = None
    asset_id: int | None = None
    asset_name: str | None = None
    description: str | None = None


class PurchaseRequest(_CamelModel):
    """A purchase request header with all its line items.

    The single-item endpoint (GET /purchase-requests/{id}) returns the full
    record including ``items`` and attachments.  The list endpoint may return
    a lighter representation.

    Attributes:
        id: Internal integer identifier.
        number: Human-readable request number.
        type_id: ID of the purchase request type.
        type_name: Display name of the type.
        status_id: ID of the current status.
        status_name: Display name of the status.
        external_number: External reference number from a procurement system.
        description: Free-text notes.
        assigned_user_id: ID of the responsible user.
        assigned_user_name: Display name of the responsible user.
        assigned_team_id: ID of the responsible team.
        assigned_team_name: Display name of the responsible team.
        created_at: UTC timestamp of record creation.
        updated_at: UTC timestamp of the last modification.
        items: Line items included in this request.
    """

    id: int
    number: str | None = None
    type_id: int | None = None
    type_name: str | None = None
    status_id: int | None = None
    status_name: str | None = None
    external_number: str | None = None
    description: str | None = None
    assigned_user_id: int | None = None
    assigned_user_name: str | None = None
    assigned_team_id: int | None = None
    assigned_team_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    items: list[PurchaseRequestItem] | None = None


class UpdatedPurchaseRequestParams(_CamelModel):
    """Request body for partially updating a purchase request (PATCH /purchase-requests/{id}).

    All fields are optional; only provided fields are updated.  Pass ``null``
    to explicitly clear a field.

    Attributes:
        type_id: New type ID.
        status_id: New status ID.
        external_number: New external reference number.
        description: New notes.
        assigned_user_id: New responsible user ID.
        assigned_team_id: New responsible team ID.
    """

    type_id: int | None = None
    status_id: int | None = None
    external_number: str | None = None
    description: str | None = None
    assigned_user_id: int | None = None
    assigned_team_id: int | None = None
