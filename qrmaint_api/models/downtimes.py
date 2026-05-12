"""Pydantic models for the Downtimes domain."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from .common import _CamelModel


class DowntimeStatus(str, Enum):
    """Planned vs. unplanned classification for an asset downtime."""

    PLANNED = "PLANNED"
    UNPLANNED = "UNPLANNED"


class Downtime(_CamelModel):
    """An asset downtime event recorded in QrMaint."""

    id: int
    asset_id: int | None = None
    asset_external_id: str | None = None
    parent_asset_id: int | None = None
    parent_asset_external_id: str | None = None
    asset_name: str | None = None
    asset_number: str | None = None
    work_id: int | None = None
    status: DowntimeStatus | None = None
    is_active: bool | None = None
    start_datetime: datetime | None = None
    duration_hours: int | None = None
    duration_minutes: int | None = None
    duration_seconds: int | None = None
    total_duration_in_seconds: int | None = None
    remarks: str | None = None
    created_user_name: str | None = None
    created_user_id: int | None = None
    created_datetime: datetime | None = None
    failure_code: str | None = None
    external_failure_code: str | None = None


class DowntimeParams(_CamelModel):
    """Request body for recording a new downtime event (POST /downtimes).

    Attributes:
        start_datetime: Required downtime start timestamp (ISO 8601).
        status: Required downtime classification (PLANNED or UNPLANNED).
        asset_id: Asset internal ID (required if asset_external_id not provided).
        asset_external_id: Asset external ID (alternative to asset_id).
        duration_in_seconds: Optional duration; omit to leave the downtime active.
        work_id: Optional associated work order ID.
        remarks: Optional free-text remarks.
    """

    start_datetime: datetime
    status: DowntimeStatus
    asset_id: int | None = None
    asset_external_id: str | None = None
    duration_in_seconds: int | None = None
    work_id: int | None = None
    remarks: str | None = None
