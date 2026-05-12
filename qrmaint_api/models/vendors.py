"""Pydantic models for the Vendors domain."""
from __future__ import annotations

from .common import _CamelModel


class Vendor(_CamelModel):
    """A supplier or service vendor in QrMaint."""

    id: int
    name: str | None = None
    email: str | None = None
    service_email: str | None = None
    phone: str | None = None
    service_phone: str | None = None
    service_phone_prefix: str | None = None
    additional_info: str | None = None
    type_of_service_id: int | None = None
    type_of_service_name: str | None = None
    address: str | None = None
    address_city: str | None = None
    address_zip: str | None = None
    address_country: str | None = None


class VendorParams(_CamelModel):
    """Request body for creating a new vendor (POST /vendors).

    Attributes:
        name: Required vendor name.
        email: Optional vendor email.
        service_email: Optional service email.
        phone: Optional phone number.
        service_phone: Optional service phone number.
        service_phone_prefix: Optional service phone prefix (max 6 chars).
        additional_info: Optional additional information.
        type_of_service_id: Optional type of service dictionary item ID.
        address: Optional address.
        address_city: Optional city.
        address_country: Optional country.
        address_zip: Optional postal code.
    """

    name: str
    email: str | None = None
    service_email: str | None = None
    phone: str | None = None
    service_phone: str | None = None
    service_phone_prefix: str | None = None
    additional_info: str | None = None
    type_of_service_id: int | None = None
    address: str | None = None
    address_city: str | None = None
    address_country: str | None = None
    address_zip: str | None = None


class UpdatedVendorParams(_CamelModel):
    """Request body for partially updating a vendor (PATCH /vendors/{vendorId}).

    All fields are optional; only provided fields are updated.
    """

    name: str | None = None
    email: str | None = None
    service_email: str | None = None
    phone: str | None = None
    service_phone: str | None = None
    service_phone_prefix: str | None = None
    additional_info: str | None = None
    type_of_service_id: int | None = None
    address: str | None = None
    address_city: str | None = None
    address_country: str | None = None
    address_zip: str | None = None
