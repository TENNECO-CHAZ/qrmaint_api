"""Pydantic models for the Assets domain."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .common import EmbeddedAttachment, EmbeddedTag, _CamelModel


class Asset(_CamelModel):
    """A physical asset registered in QrMaint.

    Attributes:
        id: Internal integer identifier.
        external_id: Caller-supplied external identifier for integration use.
        number: Asset number (e.g. ``"EQ-1234"``).
        name: Human-readable asset name.
        description: Free-text description.
        additional_info: Additional free-text information.
        client_id: ID of the owning client/tenant.
        parent_id: ID of the parent asset in the hierarchy.
        parent_external_id: External ID of the parent asset.
        parent_name: Display name of the parent asset.
        url: QrMaint URL for this asset.
        created_datetime: UTC timestamp of record creation.
        modified_datetime: UTC timestamp of the last modification.
        created_user_id: ID of the user who created the record.
        modified_user_id: ID of the user who last modified the record.
        manufacturer_id: ID of the manufacturer dictionary item.
        manufacturer_name: Display name of the manufacturer.
        model: Manufacturer model name.
        internal_number: Internal reference number.
        serial_number: Manufacturer serial number.
        type_id: ID of the asset type dictionary item.
        type_name: Display name of the asset type.
        is_public_request: Whether public maintenance requests are enabled.
        criticality_id: ID of the criticality level dictionary item.
        criticality_name: Display name of the criticality level.
        cost_account_id: ID of the associated cost account.
        cost_account_name: Display name of the cost account.
        vendor_id: ID of the associated vendor.
        vendor_name: Display name of the vendor.
        status_id: ID of the current status dictionary item.
        status_name: Display name of the current status.
        production_date: Date the asset entered production.
        installation_date: Date the asset was installed.
        warranty_date: Warranty expiration date.
        init_price: Initial purchase price.
        is_parent_address: Whether the asset inherits its parent's address.
        address_id: ID of the address record.
        address: Street address line.
        address_city: City.
        address_state: State or province.
        address_zip: Postal code.
        address_country: Country.
        address_latitude: GPS latitude.
        address_longitude: GPS longitude.
        tags: Tags attached to the asset.
        attachments: Files attached to the asset.
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
        external_id: Optional external identifier.
        description: Optional free-text description.
        additional_info: Optional additional information.
        parent_id: Optional parent asset ID.
        location_id: Optional location ID.
        model: Optional manufacturer model.
        serial_number: Optional serial number.
        manufacturer_id: Optional manufacturer dictionary item ID.
        type_id: Optional asset type dictionary item ID.
        criticality_id: Optional criticality dictionary item ID.
        vendor_id: Optional vendor ID.
        status_id: Optional status dictionary item ID.
        production_date: Optional production date (ISO 8601).
        installation_date: Optional installation date (ISO 8601).
        warranty_date: Optional warranty expiration date (ISO 8601).
        init_price: Optional initial purchase price.
    """

    name: str
    external_id: str | None = None
    description: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    location_id: int | None = None
    model: str | None = None
    serial_number: str | None = None
    manufacturer_id: int | None = None
    type_id: int | None = None
    criticality_id: int | None = None
    vendor_id: int | None = None
    status_id: int | None = None
    production_date: datetime | None = None
    installation_date: datetime | None = None
    warranty_date: datetime | None = None
    init_price: float | None = None


class UpdatedAssetParams(_CamelModel):
    """Request body for partially updating an asset (PUT /assets/{id}).

    All fields are optional; only provided fields are updated.
    Use ``null`` to clear a field.

    Attributes:
        name: New asset name.
        external_id: New external identifier.
        description: New description.
        additional_info: New additional information.
        parent_id: New parent asset ID.
        location_id: New location ID.
        model: New manufacturer model.
        serial_number: New serial number.
        manufacturer_id: New manufacturer dictionary item ID.
        type_id: New asset type dictionary item ID.
        criticality_id: New criticality dictionary item ID.
        vendor_id: New vendor ID.
        status_id: New status dictionary item ID.
        production_date: New production date (ISO 8601).
        installation_date: New installation date (ISO 8601).
        warranty_date: New warranty expiration date (ISO 8601).
        init_price: New initial purchase price.
    """

    name: str | None = None
    external_id: str | None = None
    description: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    location_id: int | None = None
    model: str | None = None
    serial_number: str | None = None
    manufacturer_id: int | None = None
    type_id: int | None = None
    criticality_id: int | None = None
    vendor_id: int | None = None
    status_id: int | None = None
    production_date: datetime | None = None
    installation_date: datetime | None = None
    warranty_date: datetime | None = None
    init_price: float | None = None


class AssetPlannedProductionTime(_CamelModel):
    """Planned production time record for an asset (BETA endpoint).

    Attributes:
        asset_id: ID of the asset this record belongs to.
        planned_production_time: Planned production time value.
        unit: Unit of measurement for the time value.
    """

    asset_id: int
    planned_production_time: float | None = None
    unit: str | None = None
