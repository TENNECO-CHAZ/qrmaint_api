"""Pydantic models for the Locations domain."""
from __future__ import annotations

from datetime import datetime

from .common import EmbeddedAttachment, _CamelModel


class Location(_CamelModel):
    """A physical location node in the QrMaint location hierarchy.

    Attributes:
        id: Internal integer identifier.
        external_id: Caller-supplied external identifier.
        number: Location number (e.g. ``"FA-1234"``).
        name: Human-readable location name.
        additional_info: Additional free-text information.
        client_id: ID of the owning client/tenant.
        parent_id: ID of the parent location (``None`` for root nodes).
        parent_external_id: External ID of the parent location.
        located_at_id: ID of the asset or area this location is situated at.
        created_datetime: UTC timestamp of record creation.
        modified_datetime: UTC timestamp of the last modification.
        created_user_id: ID of the user who created the record.
        modified_user_id: ID of the user who last modified the record.
        type_id: ID of the location type dictionary item.
        type_name: Display name of the location type.
        cost_account_id: ID of the associated cost account.
        cost_account_name: Display name of the cost account.
        is_public_request: Whether public maintenance requests are enabled.
        is_parent_address: Whether the location inherits its parent's address.
        address_id: ID of the address record.
        address: Street address line.
        address_city: City.
        address_state: State or province.
        address_zip: Postal code.
        address_country: Country.
        address_latitude: GPS latitude.
        address_longitude: GPS longitude.
        attachments: Files attached to the location.
    """

    id: int
    external_id: str | None = None
    number: str | None = None
    name: str
    additional_info: str | None = None
    client_id: int | None = None
    parent_id: int | None = None
    parent_external_id: str | None = None
    located_at_id: int | None = None
    created_datetime: datetime | None = None
    modified_datetime: datetime | None = None
    created_user_id: int | None = None
    modified_user_id: int | None = None
    type_id: int | None = None
    type_name: str | None = None
    cost_account_id: int | None = None
    cost_account_name: str | None = None
    is_public_request: bool | None = None
    is_parent_address: bool | None = None
    address_id: int | None = None
    address: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    address_country: str | None = None
    address_latitude: float | None = None
    address_longitude: float | None = None
    attachments: list[EmbeddedAttachment] = []


class LocationParams(_CamelModel):
    """Request body for creating a new location (POST /locations).

    Attributes:
        name: Required location name.
        external_id: Optional external identifier.
        additional_info: Optional additional information.
        parent_id: Optional parent location ID (omit for root locations).
        located_at_id: Optional ID of the asset or area this location is situated at.
        type_id: Optional location type dictionary item ID.
        cost_account_id: Optional cost account ID.
    """

    name: str
    external_id: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    located_at_id: int | None = None
    type_id: int | None = None
    cost_account_id: int | None = None


class UpdatedLocationParams(_CamelModel):
    """Request body for partially updating a location (PUT /locations/{id}).

    All fields are optional; only provided fields are updated.
    Use ``null`` to clear a field.

    Attributes:
        name: New location name.
        external_id: New external identifier.
        additional_info: New additional information.
        parent_id: New parent location ID.
        located_at_id: New asset or area ID this location is situated at.
        type_id: New location type dictionary item ID.
        cost_account_id: New cost account ID.
    """

    name: str | None = None
    external_id: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    located_at_id: int | None = None
    type_id: int | None = None
    cost_account_id: int | None = None
