"""Pydantic models for the Andon Calls domain."""

from datetime import datetime

from .common import _CamelModel


class AndonCallType(_CamelModel):
    """A category/type that can be assigned to an andon call.

    Attributes:
        id: Internal integer identifier.
        name: Type name displayed in the UI.
        color: Hex colour code associated with this type.
        description: Optional description of when to use this type.
    """

    id: int
    name: str
    color: str | None = None
    description: str | None = None


class AndonCall(_CamelModel):
    """An andon (alert) call raised on the shop floor.

    Attributes:
        id: Internal integer identifier.
        asset_id: ID of the asset the call is associated with.
        asset_name: Display name of the associated asset.
        type_id: ID of the andon call type.
        type_name: Display name of the andon call type.
        status: Current status of the call (e.g. ``"OPEN"``, ``"RESOLVED"``).
        description: Free-text description of the issue.
        created_at: UTC timestamp when the call was raised.
        resolved_at: UTC timestamp when the call was resolved.
        created_by: Name or ID of the user who raised the call.
    """

    id: int
    asset_id: int | None = None
    asset_name: str | None = None
    type_id: int | None = None
    type_name: str | None = None
    status: str | None = None
    description: str | None = None
    created_at: datetime | None = None
    resolved_at: datetime | None = None
    created_by: str | None = None
