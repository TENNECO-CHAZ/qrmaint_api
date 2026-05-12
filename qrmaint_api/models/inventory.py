"""Pydantic models for the Inventory domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class InventoryDocument(_CamelModel):
    """An inventory document (receipt, issue, movement, correction, etc.)."""

    id: int
    work_id: int | None = None
    number: str | None = None
    invoice_number: str | None = None
    document_type_id: int | None = None
    document_type_name: str | None = None
    document_date: datetime | None = None
    supplier_id: int | None = None
    supplier_name: str | None = None
    currency_code: str | None = None
    currency_rate: float | None = None
    currency_rate_date: datetime | None = None
    warehouse_id: int | None = None
    warehouse_name: str | None = None
    warehouse_external_id: str | None = None
    transfer_warehouse_id: int | None = None
    transfer_warehouse_name: str | None = None
    transfer_warehouse_external_id: str | None = None
    document_total_price: float | None = None
    cost_account_id: int | None = None
    cost_account_name: str | None = None
    cost_account_external_id: str | None = None
    remarks: str | None = None
    created_user_id: int | None = None
    created_user_name: str | None = None
    created_datetime: datetime | None = None


class InventoryDocumentParams(_CamelModel):
    """Request body for creating a new inventory document (POST /inventory-documents).

    Attributes:
        document_type_id: Required document type (ADD, GET, CORRECTION, MOVEMENT).
        document_date: Required document date (ISO 8601).
        warehouse_id: Warehouse internal ID (required if warehouse_external_id not provided).
        warehouse_external_id: Warehouse external ID (alternative to warehouse_id).
        invoice_number: Optional invoice reference number.
        supplier_id: Optional supplier ID.
        currency_code: Optional ISO 4217 currency code (max 3 chars).
        currency_rate: Optional currency exchange rate.
        currency_rate_date: Optional date for the exchange rate.
        transfer_warehouse_id: Optional destination warehouse ID (for MOVEMENT type).
        transfer_warehouse_external_id: Optional destination warehouse external ID.
        cost_account_id: Optional cost account ID.
        cost_account_external_id: Optional cost account external ID.
        remarks: Optional free-text remarks.
    """

    document_type_id: str
    document_date: datetime
    warehouse_id: int | None = None
    warehouse_external_id: str | None = None
    invoice_number: str | None = None
    supplier_id: int | None = None
    currency_code: str | None = None
    currency_rate: float | None = None
    currency_rate_date: datetime | None = None
    transfer_warehouse_id: int | None = None
    transfer_warehouse_external_id: str | None = None
    cost_account_id: int | None = None
    cost_account_external_id: str | None = None
    remarks: str | None = None


class InventoryDocumentItem(_CamelModel):
    """A line item within an inventory document."""

    id: int
    part_id: int | None = None
    part_external_id: str | None = None
    part_name: str | None = None
    part_number: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    unit_of_measure_id: int | None = None
    unit_of_measure_name: str | None = None
    unit_of_measure_external_id: str | None = None
    currency_code: str | None = None


class NewInventoryDocumentItemParams(_CamelModel):
    """Request body for adding a line item to an inventory document.

    Attributes:
        quantity: Required quantity to move.
        unit_price: Required unit price for valuation.
        part_id: Part internal ID (required if part_external_id not provided).
        part_external_id: Part external ID (alternative to part_id).
    """

    quantity: float
    unit_price: float
    part_id: int | None = None
    part_external_id: str | None = None


class InventoryStockItem(_CamelModel):
    """A single item in an inventory stock adjustment request."""

    inventory_id: int
    part_id: int
    quantity: float
    unit_price: float
    minimum_quantity: float | None = None
    maximum_quantity: float | None = None
    storage_place_id: int | None = None


class InventoryStockAdjustingParams(_CamelModel):
    """Request body for a bulk inventory stock adjustment (PUT /inventory-stocks/adjust-items)."""

    inventory_stock_items_list: list[InventoryStockItem]


class InventoryStockLog(_CamelModel):
    """A historical inventory stock movement log entry (deprecated endpoint)."""

    id: int
    action_date: datetime | None = None
    inventory_stock_item_unit_price: float | None = None
    stock_item_id: int | None = None
    inventory_name: str | None = None
    inventory_action_name: str | None = None
    inventory_action_id: int | None = None
    created_datetime: datetime | None = None
    quantity: int | None = None
    part_id: int | None = None
    part_external_id: str | None = None
    part_name: str | None = None
    work_id: int | None = None
    work_number: str | None = None
    created_by_full_name: str | None = None
    received_by_full_name: str | None = None
    unit_of_measure_name: str | None = None
    change_value: str | None = None
    document_id: int | None = None
    document_number: str | None = None
    cost_account_id: int | None = None
    cost_account_name: str | None = None
