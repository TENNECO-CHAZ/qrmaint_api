"""Pydantic models for the Production Areas domain."""

from datetime import datetime

from .common import EmbeddedAttachment, EmbeddedTag, _CamelModel


class ProductionArea(_CamelModel):
    """A production area node in the QrMaint plant hierarchy.

    Attributes:
        id: Internal integer identifier.
        external_id: Caller-supplied external identifier.
        number: Area number (e.g. ``"FA-1234"``).
        name: Human-readable area name.
        additional_info: Additional free-text information.
        client_id: ID of the owning client/tenant.
        parent_id: ID of the parent location or area.
        parent_external_id: External ID of the parent.
        located_at_id: ID of the asset or location this area is situated at.
        created_datetime: UTC timestamp of record creation.
        modified_datetime: UTC timestamp of the last modification.
        created_user_id: ID of the user who created the record.
        modified_user_id: ID of the user who last modified the record.
        is_public_request: Whether public maintenance requests are enabled.
        is_parent_address: Whether the area inherits its parent's address.
        cost_account_id: ID of the associated cost account.
        cost_account_name: Display name of the cost account.
        address_id: ID of the address record.
        address: Street address line.
        address_city: City.
        address_state: State or province.
        address_zip: Postal code.
        address_country: Country.
        address_latitude: GPS latitude.
        address_longitude: GPS longitude.
        tags: Tags attached to the area.
        attachments: Files attached to the area.
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
    is_public_request: bool | None = None
    is_parent_address: bool | None = None
    cost_account_id: int | None = None
    cost_account_name: str | None = None
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


class ProductionAreaParams(_CamelModel):
    """Request body for creating a new production area (POST /production-areas).

    Attributes:
        name: Required area name.
        external_id: Optional external identifier.
        additional_info: Optional additional information.
        parent_id: Optional parent location or area ID.
        located_at_id: Optional ID of the asset or location this area is situated at.
        cost_account_id: Optional cost account ID.
        type_id: Optional area type dictionary item ID (used for filtering).
    """

    name: str
    external_id: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    located_at_id: int | None = None
    cost_account_id: int | None = None
    type_id: int | None = None


class UpdatedProductionAreaParams(_CamelModel):
    """Request body for partially updating a production area (PUT /production-areas/{id}).

    All fields are optional; only provided fields are updated.
    Use ``null`` to clear a field.

    Attributes:
        name: New area name.
        external_id: New external identifier.
        additional_info: New additional information.
        parent_id: New parent location or area ID.
        located_at_id: New asset or location ID this area is situated at.
        cost_account_id: New cost account ID.
        type_id: New area type dictionary item ID.
    """

    name: str | None = None
    external_id: str | None = None
    additional_info: str | None = None
    parent_id: int | None = None
    located_at_id: int | None = None
    cost_account_id: int | None = None
    type_id: int | None = None
