"""Pydantic models for the Parts (spare parts / inventory items) domain."""
from __future__ import annotations

from datetime import datetime

from .common import EmbeddedAttachment, EmbeddedTag, _CamelModel


class EmbeddedSupplier(_CamelModel):
    """A supplier embedded in a part list/detail response (PartSupplierSimple).

    Attributes:
        id: Internal supplier identifier.
        name: Supplier display name.
        part_number: Supplier-specific part number.
        is_default: Whether this is the preferred/default supplier.
    """

    id: int
    name: str | None = None
    part_number: str | None = None
    is_default: bool | None = None


class PartSupplier(_CamelModel):
    """A supplier returned by GET /parts/{partId}/suppliers.

    Attributes:
        id: Internal supplier identifier.
        name: Supplier display name.
        part_number: Supplier-specific part number.
        is_default: Whether this is the preferred/default supplier.
        created_datetime: UTC timestamp of record creation.
        modified_datetime: UTC timestamp of the last modification.
        created_user_id: ID of the user who created the record.
        modified_user_id: ID of the user who last modified the record.
    """

    id: int
    name: str | None = None
    part_number: str | None = None
    is_default: bool | None = None
    created_datetime: datetime | None = None
    modified_datetime: datetime | None = None
    created_user_id: int | None = None
    modified_user_id: int | None = None


class Part(_CamelModel):
    """A spare part or consumable item tracked in QrMaint inventory.

    Attributes:
        id: Internal integer identifier.
        name: Human-readable part name.
        number: Part number (e.g. ``"PR-1234"``).
        unit_of_measure_id: ID of the unit of measure.
        unit_of_measure_name: Display name of the unit of measure.
        unit_of_measure_external_id: External ID of the unit of measure.
        manufacturer_id: ID of the manufacturer.
        manufacturer_name: Display name of the manufacturer.
        manufacturer_external_id: External ID of the manufacturer.
        manufacturer_part_number: Manufacturer-assigned part number.
        preferred_supplier_id: ID of the preferred supplier.
        preferred_supplier_name: Display name of the preferred supplier.
        supplier_part_number: Preferred supplier's part number.
        additional_info: Free-text additional information.
        client_id: ID of the owning client.
        bar_code: Barcode string.
        is_active: Whether the part is active.
        external_id: Caller-supplied external identifier.
        type_id: ID of the part type.
        type_name: Display name of the part type.
        is_critical: Whether the part is flagged as critical.
        created_datetime: UTC timestamp of record creation.
        modified_datetime: UTC timestamp of the last modification.
        created_user_id: ID of the user who created the record.
        modified_user_id: ID of the user who last modified the record.
        suppliers: Suppliers associated with this part.
        tags: Tags attached to this part.
        attachments: Files attached to this part.
    """

    id: int
    name: str | None = None
    number: str | None = None
    unit_of_measure_id: int | None = None
    unit_of_measure_name: str | None = None
    unit_of_measure_external_id: str | None = None
    manufacturer_id: int | None = None
    manufacturer_name: str | None = None
    manufacturer_external_id: str | None = None
    manufacturer_part_number: str | None = None
    preferred_supplier_id: int | None = None
    preferred_supplier_name: str | None = None
    supplier_part_number: str | None = None
    additional_info: str | None = None
    client_id: int | None = None
    bar_code: str | None = None
    is_active: bool | None = None
    external_id: str | None = None
    type_id: int | None = None
    type_name: str | None = None
    is_critical: bool | None = None
    created_datetime: datetime | None = None
    modified_datetime: datetime | None = None
    created_user_id: int | None = None
    modified_user_id: int | None = None
    suppliers: list[EmbeddedSupplier] = []
    tags: list[EmbeddedTag] = []
    attachments: list[EmbeddedAttachment] = []


class PartParams(_CamelModel):
    """Request body for creating a new part (POST /parts).

    Attributes:
        name: Required part name.
        external_id: Optional external identifier.
        type_id: ID of the part type.
        unit_of_measure_id: ID of the unit of measure.
        unit_of_measure_external_id: External ID of the unit of measure.
        manufacturer_id: ID of the manufacturer.
        manufacturer_external_id: External ID of the manufacturer.
        manufacturer_part_number: Manufacturer-assigned part number.
        bar_code: Barcode string.
        additional_info: Free-text additional information.
        is_critical: Whether the part should be flagged as critical.
    """

    name: str
    external_id: str | None = None
    type_id: int | None = None
    unit_of_measure_id: int | None = None
    unit_of_measure_external_id: str | None = None
    manufacturer_id: int | None = None
    manufacturer_external_id: str | None = None
    manufacturer_part_number: str | None = None
    bar_code: str | None = None
    additional_info: str | None = None
    is_critical: bool | None = None


class PartSupplierParams(_CamelModel):
    """Request body for adding a supplier to a part (POST /parts/{partId}/suppliers).

    Attributes:
        id: Internal supplier ID.
        part_number: Supplier-specific part number.
        is_default: Whether this supplier should be set as the default.
    """

    id: int
    part_number: str | None = None
    is_default: bool | None = None


class PartSupplierUpdateParams(_CamelModel):
    """Request body for updating a part supplier (PATCH /parts/{partId}/suppliers/{supplierId}).

    Attributes:
        part_number: Supplier-specific part number.
        is_default: Whether this supplier should be set as the default.
    """

    part_number: str | None = None
    is_default: bool | None = None


class PartUpdateParams(_CamelModel):
    """Request body for updating an existing part (PUT /parts/{id}).

    All fields are optional — omitted fields are left unchanged.

    Attributes:
        name: Part name.
        external_id: External identifier.
        type_id: ID of the part type.
        unit_of_measure_id: ID of the unit of measure.
        unit_of_measure_external_id: External ID of the unit of measure.
        manufacturer_id: ID of the manufacturer.
        manufacturer_external_id: External ID of the manufacturer.
        manufacturer_part_number: Manufacturer-assigned part number.
        bar_code: Barcode string.
        additional_info: Free-text additional information.
        is_critical: Whether the part should be flagged as critical.
    """

    name: str | None = None
    external_id: str | None = None
    type_id: int | None = None
    unit_of_measure_id: int | None = None
    unit_of_measure_external_id: str | None = None
    manufacturer_id: int | None = None
    manufacturer_external_id: str | None = None
    manufacturer_part_number: str | None = None
    bar_code: str | None = None
    additional_info: str | None = None
    is_critical: bool | None = None
