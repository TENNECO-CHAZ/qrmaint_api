"""Pydantic models for the Shifts domain."""
from __future__ import annotations

from .common import _CamelModel


class Shift(_CamelModel):
    """A work shift defined in QrMaint.

    Shifts can be assigned to work orders to indicate during which scheduled
    window the maintenance activity should be performed.

    Attributes:
        id: Internal integer identifier.
        name: Human-readable shift name.
        start_time: Shift start time as a string (e.g. ``"06:00"``).
        end_time: Shift end time as a string (e.g. ``"14:00"``).
        description: Optional free-text description.
        active: Whether the shift is currently selectable.
    """

    id: int
    name: str
    start_time: str | None = None
    end_time: str | None = None
    description: str | None = None
    active: bool | None = None
