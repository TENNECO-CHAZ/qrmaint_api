"""Pydantic models for the Downtimes domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class Downtime(_CamelModel):
    """A downtime event recorded for an asset.

    Attributes:
        id: Internal integer identifier.
        asset_id: ID of the asset that was down.
        asset_name: Display name of the asset.
        start_date: UTC timestamp when the downtime began.
        end_date: UTC timestamp when the downtime ended (``None`` if ongoing).
        duration_minutes: Computed duration in minutes.
        reason: Short reason label.
        description: Free-text description of the downtime event.
        failure_code: Failure code label applied to this downtime.
        created_at: UTC timestamp of record creation.
        updated_at: UTC timestamp of the last modification.
    """

    id: int
    asset_id: int
    asset_name: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    duration_minutes: float | None = None
    reason: str | None = None
    description: str | None = None
    failure_code: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DowntimeParams(_CamelModel):
    """Request body for recording a new downtime event (POST /downtimes).

    Attributes:
        asset_id: Required ID of the affected asset.
        start_date: Required UTC start timestamp.
        end_date: Optional UTC end timestamp (omit for open-ended downtime).
        reason: Optional reason label.
        description: Optional free-text description.
        failure_code_id: Optional failure code dictionary item ID.
    """

    asset_id: int
    start_date: datetime
    end_date: datetime | None = None
    reason: str | None = None
    description: str | None = None
    failure_code_id: int | None = None
