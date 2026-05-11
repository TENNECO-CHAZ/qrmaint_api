"""Pydantic models for the Production Lines domain."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .common import EmbeddedAttachment, EmbeddedTag, _CamelModel


class ProductionLine(_CamelModel):
    """A production line associated with a parent asset in QrMaint.

    Attributes:
        id: Internal integer identifier.
        external_id: Caller-supplied external identifier.
        number: Line number (e.g. ``"FA-1234"``).
        name: Human-readable line name.
        description: Free-text description.
        additional_info: Additional free-text information.
        client_id: ID of the owning client/tenant.
        parent_id: ID of the parent asset this line belongs to.
        parent_external_id: External ID of the parent asset.
        parent_name: Display name of the parent asset.
        url: QrMaint URL for this production line.
        created_datetime: UTC timestamp of record creation.
        modified_datetime: UTC timestamp of the last modification.
        created_user_id: ID of the user who created the record.
        modified_user_id: ID of the user who last modified the record.
        is_public_request: Whether public maintenance requests are enabled.
        cost_account_id: ID of the associated cost account.
        cost_account_name: Display name of the cost account.
        status_id: ID of the current status dictionary item.
        status_name: Display name of the current status.
        tags: Tags attached to the production line.
        attachments: Files attached to the production line.
    """

    id: int
    external_id: str | None = None
    number: str | None = None
    name: str
    description: str | None = None
    additional_info: str | None = None
    client_id: int | None = None
    parent_id: int | None = None
    parent_external_id: str | None = None
    parent_name: str | None = None
    url: str | None = Field(default=None, alias="URL")
    created_datetime: datetime | None = None
    modified_datetime: datetime | None = None
    created_user_id: int | None = None
    modified_user_id: int | None = None
    is_public_request: bool | None = None
    cost_account_id: int | None = None
    cost_account_name: str | None = None
    status_id: int | None = None
    status_name: str | None = None
    tags: list[EmbeddedTag] = []
    attachments: list[EmbeddedAttachment] = []


class ProductionLineParams(_CamelModel):
    """Request body for creating a new production line (POST /production-lines).

    Attributes:
        name: Required line name.
        external_id: Optional external identifier.
        description: Optional free-text description.
        additional_info: Optional additional information.
        parent_id: Optional parent asset ID.
        location_id: Optional location ID.
        cost_account_id: Optional cost account ID.
        status_id: Optional status dictionary item ID.
    """

    name: str
    external_id: str | None = None
    description: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    location_id: int | None = None
    cost_account_id: int | None = None
    status_id: int | None = None


class UpdatedProductionLineParams(_CamelModel):
    """Request body for partially updating a production line (PUT /production-lines/{id}).

    All fields are optional; only provided fields are updated.
    Use ``null`` to clear a field.

    Attributes:
        name: New line name.
        external_id: New external identifier.
        description: New description.
        additional_info: New additional information.
        parent_id: New parent asset ID.
        location_id: New location ID.
        cost_account_id: New cost account ID.
        status_id: New status dictionary item ID.
    """

    name: str | None = None
    external_id: str | None = None
    description: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    location_id: int | None = None
    cost_account_id: int | None = None
    status_id: int | None = None
