"""Pydantic models for the Work Requests domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class WorkRequest(_CamelModel):
    """A work request submitted by a non-maintenance user in QrMaint.

    Work requests are the intake mechanism for reporting issues.  They can be
    reviewed and promoted to full work orders by maintenance staff.

    Attributes:
        id: Internal integer identifier.
        number: Human-readable request number.
        subject: Short summary of the reported issue.
        description: Detailed free-text description of the issue.
        status_id: ID of the current lifecycle status.
        status_name: Display name of the status.
        priority_id: ID of the priority dictionary item.
        priority_name: Display name of the priority.
        asset_id: ID of the asset the issue relates to.
        asset_name: Display name of the asset.
        location_id: ID of the location where the issue was observed.
        location_name: Display name of the location.
        failure_code_id: ID of the failure-code dictionary item.
        created_at: UTC timestamp of record creation.
        updated_at: UTC timestamp of the last modification.
    """

    id: int
    number: str | None = None
    subject: str | None = None
    description: str | None = None
    status_id: int | None = None
    status_name: str | None = None
    priority_id: int | None = None
    priority_name: str | None = None
    asset_id: int | None = None
    asset_name: str | None = None
    location_id: int | None = None
    location_name: str | None = None
    failure_code_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class WorkRequestParams(_CamelModel):
    """Request body for creating a new work request (POST /work-requests).

    Attributes:
        subject: Required short summary of the issue.
        asset_id: Optional ID of the affected asset.
        location_id: Optional ID of the relevant location.
        priority_id: Optional priority dictionary item ID.
        failure_code_id: Optional failure-code dictionary item ID.
        description: Optional detailed description of the issue.
    """

    subject: str
    asset_id: int | None = None
    location_id: int | None = None
    priority_id: int | None = None
    failure_code_id: int | None = None
    description: str | None = None
