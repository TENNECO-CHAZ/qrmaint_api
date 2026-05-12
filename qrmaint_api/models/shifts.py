"""Pydantic models for the Shifts domain."""
from __future__ import annotations

from .common import _CamelModel


class Shift(_CamelModel):
    """A work shift defined in QrMaint."""

    id: int
    name: str | None = None
    start_time: str | None = None
    end_time: str | None = None
