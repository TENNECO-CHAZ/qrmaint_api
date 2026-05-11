"""Pydantic models for the Teams domain."""
from __future__ import annotations

from .common import _CamelModel


class Team(_CamelModel):
    """A maintenance team in QrMaint.

    Teams can be assigned to work orders as a group, and serve as an
    organisational unit for technicians.

    Attributes:
        id: Internal integer identifier.
        name: Human-readable team name.
        external_id: Caller-supplied external identifier.
        description: Optional free-text description.
    """

    id: int
    name: str
    external_id: str | None = None
    description: str | None = None
