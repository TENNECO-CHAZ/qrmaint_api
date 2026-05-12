"""Pydantic models for the Attachments domain."""
from __future__ import annotations

from datetime import datetime

from .common import _CamelModel


class Attachment(_CamelModel):
    """A file attachment linked to a QrMaint resource."""

    id: int
    file_name: str | None = None
    size: int | None = None
    type: str | None = None
    type_group: str | None = None
    created_datetime: datetime | None = None


class AttachmentDownloadUrl(_CamelModel):
    """A time-limited pre-signed download URL for an attachment."""

    url: str | None = None
    expires_at: datetime | None = None
