"""Pydantic models for the Work Requests domain."""
from __future__ import annotations

from datetime import datetime

from .attachments import Attachment
from .common import _CamelModel
from .work_orders import AssignedResource, AssignedTag, PriorityType


class WorkRequest(_CamelModel):
    """A work request submitted by a non-maintenance user in QrMaint."""

    id: int
    client_id: int | None = None
    created_datetime: datetime | None = None
    modified_datetime: datetime | None = None
    modified_user_id: int | None = None
    created_user_id: int | None = None
    failure_code_id: int | None = None
    failure_code_name: str | None = None
    external_failure_code: str | None = None
    subject: str | None = None
    number: str | None = None
    description: str | None = None
    status_id: int | None = None
    status_name: str | None = None
    priority: PriorityType | None = None
    assigned_assets_or_locations: list[AssignedResource] = []
    tags: list[AssignedTag] = []
    attachments: list[Attachment] = []


class WorkRequestParams(_CamelModel):
    """Request body for creating a new work request (POST /work-requests).

    Attributes:
        subject: Required short summary of the issue.
        priority: Required priority level (LOW, MEDIUM, HIGH).
        description: Optional detailed description.
        failure_code_id: Optional failure code ID.
        external_failure_code: Optional external failure code string.
        asset_or_location_id: Optional asset or location ID.
        asset_or_location_external_id: Optional asset or location external ID.
        is_breakdown: Set true to register asset downtime.
        allow_duplicate_for_failure_code_id: Set false to prevent duplicate requests.
    """

    subject: str
    priority: PriorityType
    description: str | None = None
    failure_code_id: int | None = None
    external_failure_code: str | None = None
    asset_or_location_id: int | None = None
    asset_or_location_external_id: str | None = None
    is_breakdown: bool | None = None
    allow_duplicate_for_failure_code_id: bool | None = None
