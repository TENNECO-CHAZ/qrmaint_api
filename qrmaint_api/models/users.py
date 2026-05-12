"""Pydantic models for the Users domain."""
from __future__ import annotations

from .common import _CamelModel


class User(_CamelModel):
    """A QrMaint platform user."""

    id: int
    full_name: str | None = None
    email: str | None = None
    role_id: int | None = None
    role_name: str | None = None
