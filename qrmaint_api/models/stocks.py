"""Pydantic models for the Stocks domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class Stock(_CamelModel):
    """The current stock level of a part in a specific warehouse."""

    id: int
    part_id: int | None = None
    part_external_id: str | None = None
    part_name: str | None = None
    warehouse_id: int | None = None
    warehouse_name: str | None = None
    quantity: float | None = None
    minimum_quantity: float | None = None
    reserved_quantity: float | None = None
    maximum_quantity: float | None = None
    storage_place_id: int | None = None
    storage_place_name: str | None = None
    storage_place_path: str | None = None


class UpdatedStockParams(_CamelModel):
    """Request body for partially updating a stock record (PATCH /stocks/{stockId})."""

    minimum_quantity: float | None = None
    maximum_quantity: float | None = None
    storage_place_id: int | None = None
    storage_place_text: str | None = None


class StockItem(_CamelModel):
    """A single line within a bulk stock adjustment request."""

    warehouse_id: int
    part_id: int
    quantity: float
    minimum_quantity: float
    maximum_quantity: float
    unit_price: float
    storage_place_id: int | None = None


class StockAdjustingParams(_CamelModel):
    """Request body for bulk stock adjustment (PUT /stocks/adjust-items)."""

    stock_items_list: list[StockItem]


class StockLog(_CamelModel):
    """An audit log entry recording a stock quantity change."""

    id: int
    stock_movement_datetime: datetime | None = None
    stock_movement_type_id: int | None = None
    stock_movement_type_name: str | None = None
    unit_price: float | None = None
    warehouse_name: str | None = None
    warehouse_id: int | None = None
    warehouse_external_id: str | None = None
    created_datetime: datetime | None = None
    part_id: int | None = None
    part_external_id: str | None = None
    part_name: str | None = None
    work_id: int | None = None
    work_number: str | None = None
    created_by_full_name: str | None = None
    received_by_full_name: str | None = None
    unit_of_measure_name: str | None = None
    unit_of_measure_id: int | None = None
    unit_of_measure_external_id: str | None = None
    change_value: float | None = None
    inventory_document_id: int | None = None
    inventory_document_number: str | None = None
    inventory_document_date: datetime | None = None
    inventory_document_type_id: int | None = None
    inventory_document_type_name: str | None = None
    cost_account_id: int | None = None
    cost_account_external_id: str | None = None
    cost_account_name: str | None = None
