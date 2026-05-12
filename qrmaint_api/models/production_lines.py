"""Pydantic models for the Production Lines domain."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .common import EmbeddedAttachment, EmbeddedTag, _CamelModel


class ProductionLine(_CamelModel):
    """A production line associated with a parent asset in QrMaint."""

    id: int
    external_id: str | None = None
    number: str | None = None
    name: str | None = None
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
        located_at_id: Parent asset or location internal ID.
        located_at_external_id: Parent asset or location external ID.
        is_public_request: Whether public maintenance requests are enabled.
        external_id: Optional external identifier.
        additional_info: Optional additional information.
        cost_account_id: Optional cost account ID.
        status_id: Optional status dictionary item ID.
    """

    name: str
    located_at_id: int | None = None
    located_at_external_id: str | None = None
    is_public_request: bool | None = None
    external_id: str | None = None
    additional_info: str | None = None
    cost_account_id: int | None = None
    status_id: int | None = None


class UpdatedProductionLineParams(_CamelModel):
    """Request body for partially updating a production line (PUT /production-lines/{id}).

    All fields are optional; only provided fields are updated.
    """

    name: str | None = None
    located_at_id: int | None = None
    located_at_external_id: str | None = None
    is_public_request: bool | None = None
    external_id: str | None = None
    additional_info: str | None = None
    cost_account_id: int | None = None
    status_id: int | None = None
