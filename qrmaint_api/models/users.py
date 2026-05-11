"""Pydantic models for the Users domain."""

from .common import _CamelModel


class User(_CamelModel):
    """A QrMaint platform user.

    Users can be assigned to work orders individually or as part of a team.

    Attributes:
        id: Internal integer identifier.
        name: Full display name of the user.
        email: Email address used for login and notifications.
        external_id: Caller-supplied external identifier (e.g. HR system ID).
        role: Platform role name (e.g. ``"TECHNICIAN"``, ``"MANAGER"``).
        active: Whether the account is currently enabled.
    """

    id: int
    name: str
    email: str | None = None
    external_id: str | None = None
    role: str | None = None
    active: bool | None = None
