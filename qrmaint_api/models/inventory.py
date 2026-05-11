"""Pydantic models for the Inventory domain."""

from datetime import datetime

from .common import _CamelModel


class InventoryDocument(_CamelModel):
    """An inventory document (receipt, issue, correction, etc.).

    Attributes:
        id: Internal integer identifier.
        document_number: Human-readable document reference number.
        type: Document type (e.g. ``"RECEIPT"``, ``"ISSUE"``, ``"CORRECTION"``).
        status: Current document status.
        description: Free-text description or notes.
        created_at: UTC timestamp of document creation.
        updated_at: UTC timestamp of the last modification.
        created_by: Name or ID of the user who created the document.
    """

    id: int
    document_number: str | None = None
    type: str | None = None
    status: str | None = None
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: str | None = None


class InventoryDocumentParams(_CamelModel):
    """Request body for creating a new inventory document (POST /inventory-documents).

    Attributes:
        type: Required document type identifier.
        description: Optional free-text notes.
    """

    type: str
    description: str | None = None


class InventoryDocumentItem(_CamelModel):
    """A line item within an inventory document.

    Attributes:
        id: Internal integer identifier.
        document_id: ID of the parent inventory document.
        part_id: ID of the part referenced by this line.
        part_name: Display name of the part.
        quantity: Quantity moved (positive = in, negative = out).
        unit: Unit of measurement.
    """

    id: int
    document_id: int | None = None
    part_id: int | None = None
    part_name: str | None = None
    quantity: float | None = None
    unit: str | None = None


class NewInventoryDocumentItemParams(_CamelModel):
    """Request body for adding a line item to an inventory document.

    Attributes:
        part_id: Required ID of the part to move.
        quantity: Required quantity to move.
        unit: Optional unit of measurement override.
    """

    part_id: int
    quantity: float
    unit: str | None = None


class InventoryStockLog(_CamelModel):
    """A historical stock movement log entry.

    Attributes:
        id: Internal integer identifier.
        part_id: ID of the part affected.
        part_name: Display name of the part.
        quantity_change: Signed quantity delta applied by this movement.
        quantity_after: Stock level after this movement was applied.
        reason: Human-readable reason for the movement.
        document_id: ID of the inventory document that caused the movement.
        created_at: UTC timestamp of the movement.
    """

    id: int
    part_id: int | None = None
    part_name: str | None = None
    quantity_change: float | None = None
    quantity_after: float | None = None
    reason: str | None = None
    document_id: int | None = None
    created_at: datetime | None = None


class InventoryStockAdjustingParams(_CamelModel):
    """Request body for a direct stock quantity adjustment.

    Attributes:
        part_id: Required ID of the part to adjust.
        quantity: Required new absolute stock quantity.
        reason: Optional explanation for the adjustment.
    """

    part_id: int
    quantity: float
    reason: str | None = None
