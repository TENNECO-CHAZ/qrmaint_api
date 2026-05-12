"""Pydantic models for the Failure Codes domain."""
from __future__ import annotations

from .common import _CamelModel


class FailureCode(_CamelModel):
    """A failure code used to categorise work orders and work requests."""

    id: int
    name: str | None = None
    external_failure_code: str | None = None
