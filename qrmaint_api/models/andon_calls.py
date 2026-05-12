"""Pydantic models for the Andon Calls domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class AndonCall(_CamelModel):
    """An andon (alert) call raised on the shop floor."""

    id: int
    call_type_id: int | None = None
    call_type_name: str | None = None
    call_type_color: str | None = None
    team_id: int | None = None
    asset_id: int | None = None
    parent_asset_id: int | None = None
    asset_external_id: str | None = None
    parent_asset_external_id: str | None = None
    client_id: str | None = None
    created_user_id: int | None = None
    created_datetime: datetime | None = None
    completed_user_id: int | None = None
    completed_datetime: datetime | None = None
    team_name: str | None = None
    number: str | None = None
    remarks: str | None = None
    priority: int | None = None
    duration_time_in_seconds: int | None = None
    completed_duration_time_in_seconds: str | None = None
    assigned_user_id: int | None = None
    assigned_datetime: datetime | None = None
    asset_name: str | None = None
    asset_path: str | None = None
    call_status_name: str | None = None
    assigned_user_full_name: str | None = None
    completed_user_full_name: str | None = None
    andon_panel_user_full_name: str | None = None
    is_cancelled: bool | None = None
