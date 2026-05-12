"""Pydantic models for the Locations domain."""
from __future__ import annotations

from datetime import datetime

from .common import EmbeddedAttachment, _CamelModel


class Location(_CamelModel):
    """A physical location node in the QrMaint location hierarchy."""

    id: int
    external_id: str | None = None
    number: str | None = None
    name: str | None = None
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
        located_at_id: Parent asset internal ID.
        located_at_external_id: Parent asset external ID.
        type_id: Optional location type dictionary item ID.
        is_public_request: Whether public maintenance requests are enabled.
        is_parent_address: Inherit parent's address.
        external_id: Optional external identifier.
        additional_info: Optional additional information.
        cost_account_id: Optional cost account ID.
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
    type_id: int | None = None
    is_public_request: bool | None = None
    is_parent_address: bool | None = None
    external_id: str | None = None
    additional_info: str | None = None
    cost_account_id: int | None = None
    address: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    address_country: str | None = None
    address_latitude: float | None = None
    address_longitude: float | None = None


class UpdatedLocationParams(_CamelModel):
    """Request body for partially updating a location (PUT /locations/{id}).

    All fields are optional; only provided fields are updated.
    """

    name: str | None = None
    located_at_id: int | None = None
    located_at_external_id: str | None = None
    type_id: int | None = None
    is_public_request: bool | None = None
    is_parent_address: bool | None = None
    external_id: str | None = None
    additional_info: str | None = None
    cost_account_id: int | None = None
    address: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    address_country: str | None = None
    address_latitude: float | None = None
    address_longitude: float | None = None
