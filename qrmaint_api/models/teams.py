"""Pydantic models for the Teams domain."""
from __future__ import annotations

from .common import _CamelModel


class Team(_CamelModel):
    """A maintenance team in QrMaint."""

    id: int
    name: str | None = None
    type: str | None = None
