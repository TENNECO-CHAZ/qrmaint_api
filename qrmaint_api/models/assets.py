"""Pydantic models for the Assets domain."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .common import EmbeddedAttachment, EmbeddedTag, _CamelModel


class Asset(_CamelModel):
    """A physical asset registered in QrMaint."""

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
    manufacturer_id: int | None = None
    manufacturer_name: str | None = None
    model: str | None = None
    internal_number: str | None = None
    serial_number: str | None = None
    type_id: int | None = None
    type_name: str | None = None
    is_public_request: bool | None = None
    criticality_id: int | None = None
    criticality_name: str | None = None
    cost_account_id: int | None = None
    cost_account_name: str | None = None
    vendor_id: int | None = None
    vendor_name: str | None = None
    status_id: int | None = None
    status_name: str | None = None
    production_date: datetime | None = None
    installation_date: datetime | None = None
    warranty_date: datetime | None = None
    init_price: float | None = None
    is_parent_address: bool | None = None
    address_id: int | None = None
    address: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    address_country: str | None = None
    address_latitude: float | None = None
    address_longitude: float | None = None
    tags: list[EmbeddedTag] = []
    attachments: list[EmbeddedAttachment] = []


class AssetParams(_CamelModel):
    """Request body for creating a new asset (POST /assets).

    Attributes:
        name: Required asset name.
        located_at_id: Parent asset internal ID.
        located_at_external_id: Parent asset external ID.
        external_id: Optional external identifier.
        additional_info: Optional additional information.
        manufacturer_id: Optional manufacturer dictionary item ID.
        model: Optional manufacturer model name.
        internal_number: Optional internal reference number.
        serial_number: Optional serial number.
        type_id: Optional asset type dictionary item ID.
        is_public_request: Whether public maintenance requests are enabled.
        criticality_id: Optional criticality dictionary item ID.
        cost_account_id: Optional cost account ID.
        vendor_id: Optional vendor ID.
        status_id: Optional status dictionary item ID.
        production_date: Optional production date (ISO 8601).
        installation_date: Optional installation date (ISO 8601).
        warranty_date: Optional warranty expiration date (ISO 8601).
        init_price: Optional initial purchase price.
        address: Optional street address.
        address_city: Optional city.
        address_state: Optional state.
        address_zip: Optional postal code.
        address_country: Optional country.
        address_latitude: Optional GPS latitude.
        address_longitude: Optional GPS longitude.
    """

    name: str
    located_at_id: int | None = None
    located_at_external_id: str | None = None
    external_id: str | None = None
    additional_info: str | None = None
    manufacturer_id: int | None = None
    model: str | None = None
    internal_number: str | None = None
    serial_number: str | None = None
    type_id: int | None = None
    is_public_request: bool | None = None
    criticality_id: int | None = None
    cost_account_id: int | None = None
    vendor_id: int | None = None
    status_id: int | None = None
    production_date: datetime | None = None
    installation_date: datetime | None = None
    warranty_date: datetime | None = None
    init_price: float | None = None
    address: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    address_country: str | None = None
    address_latitude: float | None = None
    address_longitude: float | None = None


class UpdatedAssetParams(_CamelModel):
    """Request body for partially updating an asset (PUT /assets/{id}).

    All fields are optional; only provided fields are updated.
    """

    name: str | None = None
    located_at_id: int | None = None
    located_at_external_id: str | None = None
    external_id: str | None = None
    additional_info: str | None = None
    manufacturer_id: int | None = None
    model: str | None = None
    internal_number: str | None = None
    serial_number: str | None = None
    type_id: int | None = None
    is_public_request: bool | None = None
    criticality_id: int | None = None
    cost_account_id: int | None = None
    vendor_id: int | None = None
    status_id: int | None = None
    production_date: datetime | None = None
    installation_date: datetime | None = None
    warranty_date: datetime | None = None
    init_price: float | None = None
    address: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    address_country: str | None = None
    address_latitude: float | None = None
    address_longitude: float | None = None


class AssetPlannedProductionTime(_CamelModel):
    """Planned production time record for an asset (BETA endpoint)."""

    planned_production_time_in_seconds: int | None = None
