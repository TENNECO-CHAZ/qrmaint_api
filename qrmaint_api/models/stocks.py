"""Pydantic models for the Stocks domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class Stock(_CamelModel):
    """The current stock level of a part in a specific warehouse.

    Attributes:
        id: Internal integer identifier of the stock record.
        part_id: ID of the part this stock entry tracks.
        part_external_id: External identifier of the part.
        part_name: Display name of the part.
        warehouse_id: ID of the warehouse holding this stock.
        warehouse_name: Display name of the warehouse.
        quantity: Current on-hand quantity.
        minimum_quantity: Reorder threshold; alerts trigger below this level.
        maximum_quantity: Upper stocking limit.
        reserved_quantity: Quantity reserved for open work orders.
        storage_place_id: ID of the specific storage location within the warehouse.
        storage_place_name: Display name of the storage location.
        storage_place_path: Full hierarchical path to the storage location.
        storage_place_text: Free-text storage location override.
    """

    id: int
    part_id: int | None = None
    part_external_id: str | None = None
    part_name: str | None = None
    warehouse_id: int | None = None
    warehouse_name: str | None = None
    quantity: float | None = None
    minimum_quantity: float | None = None
    maximum_quantity: float | None = None
    reserved_quantity: float | None = None
    storage_place_id: int | None = None
    storage_place_name: str | None = None
    storage_place_path: str | None = None
    storage_place_text: str | None = None


class UpdatedStockParams(_CamelModel):
    """Request body for partially updating a stock record (PATCH /stocks/{stockId}).

    All fields are optional; only provided fields are updated.

    Attributes:
        minimum_quantity: New reorder threshold.
        maximum_quantity: New upper stocking limit.
        storage_place_id: New storage location ID within the warehouse.
        storage_place_text: New free-text storage location override.
    """

    minimum_quantity: float | None = None
    maximum_quantity: float | None = None
    storage_place_id: int | None = None
    storage_place_text: str | None = None


class StockAdjustingItem(_CamelModel):
    """A single line within a bulk stock adjustment request.

    Attributes:
        warehouse_id: ID of the target warehouse.
        part_id: ID of the part to adjust.
        quantity: New absolute on-hand quantity after the adjustment.
        minimum_quantity: New reorder threshold to apply.
        maximum_quantity: New upper stocking limit to apply.
        unit_price: Unit cost used for valuation.
        storage_place_id: Optional storage location ID within the warehouse.
    """

    warehouse_id: int
    part_id: int
    quantity: float
    minimum_quantity: float
    maximum_quantity: float
    unit_price: float
    storage_place_id: int | None = None


class StockAdjustingParams(_CamelModel):
    """Request body for bulk stock adjustment (PUT /stocks/adjust-items).

    Attributes:
        items: One or more stock adjustment line items to process.
    """

    items: list[StockAdjustingItem]


class StockLog(_CamelModel):
    """An audit log entry recording a stock quantity change.

    Attributes:
        id: Internal integer identifier.
        part_id: ID of the part whose stock changed.
        part_name: Display name of the part.
        part_external_id: External identifier of the part.
        warehouse_id: ID of the warehouse where the change occurred.
        warehouse_name: Display name of the warehouse.
        quantity_change: Signed delta applied to the stock level.
        quantity_after: Stock level immediately after the change.
        stock_movement_type_id: ID of the movement type dictionary item.
        stock_movement_type_name: Display name of the movement type.
        inventory_document_id: ID of the inventory document that triggered this change.
        inventory_document_type_id: Type ID of the triggering document.
        created_at: UTC timestamp of the stock movement.
    """

    id: int
    part_id: int | None = None
    part_name: str | None = None
    part_external_id: str | None = None
    warehouse_id: int | None = None
    warehouse_name: str | None = None
    quantity_change: float | None = None
    quantity_after: float | None = None
    stock_movement_type_id: int | None = None
    stock_movement_type_name: str | None = None
    inventory_document_id: int | None = None
    inventory_document_type_id: int | None = None
    created_at: datetime | None = None
