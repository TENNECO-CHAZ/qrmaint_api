"""Pydantic models for the Purchase Requests domain."""
from __future__ import annotations

from datetime import datetime

from .attachments import Attachment
from .common import _CamelModel


class PurchaseRequestItem(_CamelModel):
    """A single line item within a purchase request."""

    id: int | None = None
    quantity: int | None = None
    currency_code: str | None = None
    unit_amount: float | None = None
    total_amount: float | None = None
    unit_of_measure_id: int | None = None
    unit_of_measure_name: str | None = None
    cost_account_id: int | None = None
    cost_account_name: str | None = None
    service_type_id: int | None = None
    service_type_name: str | None = None
    supplier_id: int | None = None
    supplier_name: str | None = None
    asset_id: int | None = None
    asset_name: str | None = None
    part_id: int | None = None
    part_external_id: str | None = None
    part_name: str | None = None
    part_number: str | None = None
    is_not_existing_part: bool | None = None
    not_existing_part_name: str | None = None
    not_existing_part_info: str | None = None
    service_description: str | None = None
    other_p_r_description: str | None = None


class PurchaseRequest(_CamelModel):
    """A purchase request header with all its line items."""

    id: int
    number: str | None = None
    type_name: str | None = None
    type_id: int | None = None
    created_datetime: datetime | None = None
    created_datetime_by_month: str | None = None
    created_user_name: str | None = None
    status_name: str | None = None
    status_id: int | None = None
    reason: str | None = None
    due_date: datetime | None = None
    is_critical: bool | None = None
    planned_delivery_date: datetime | None = None
    cost_period_year: int | None = None
    cost_period_month: int | None = None
    cost_period_id: int | None = None
    assigned_user_id: int | None = None
    assigned_user_name: str | None = None
    assigned_team_id: int | None = None
    assigned_team_name: str | None = None
    purpose_id: int | None = None
    purchase_request_external_number: str | None = None
    purchase_order_external_number: str | None = None
    remarks: str | None = None
    is_self_purchase: bool | None = None
    purpose_name: str | None = None
    related_work_number: str | None = None
    related_work_id: int | None = None
    items: list[PurchaseRequestItem] | None = None
    attachments: list[Attachment] | None = None


class UpdatedPurchaseRequestParams(_CamelModel):
    """Request body for partially updating a purchase request (PATCH /purchase-requests/{id}).

    All fields are optional; only provided fields are updated.
    """

    type_id: int | None = None
    status_id: int | None = None
    reason: str | None = None
    due_date: datetime | None = None
    is_critical: bool | None = None
    planned_delivery_date: datetime | None = None
    assigned_user_id: int | None = None
    assigned_team_id: int | None = None
    purpose_id: int | None = None
    purchase_request_external_number: str | None = None
    purchase_order_external_number: str | None = None
    remarks: str | None = None
    is_self_purchase: bool | None = None
    related_work_id: int | None = None
