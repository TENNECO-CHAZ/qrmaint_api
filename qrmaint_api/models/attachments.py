"""Pydantic models for the Attachments domain."""

from datetime import datetime

from .common import _CamelModel


class Attachment(_CamelModel):
    """A file attachment linked to a QrMaint resource.

    Attachments can belong to assets, work orders, or other entities.

    Attributes:
        id: Internal integer identifier.
        name: Display name of the attachment.
        file_name: Original file name including extension.
        content_type: MIME type (e.g. ``"image/jpeg"``, ``"application/pdf"``).
        size: File size in bytes.
        resource_type: Type of the parent resource (e.g. ``"ASSET"``).
        resource_id: ID of the parent resource.
        created_at: UTC timestamp of upload.
        created_by: Name or ID of the uploading user.
    """

    id: int
    name: str | None = None
    file_name: str | None = None
    content_type: str | None = None
    size: int | None = None
    resource_type: str | None = None
    resource_id: int | None = None
    created_at: datetime | None = None
    created_by: str | None = None


class AttachmentDownloadUrl(_CamelModel):
    """A time-limited pre-signed download URL for an attachment.

    Attributes:
        url: The pre-signed URL that can be used to download the file.
        expires_at: UTC timestamp after which the URL becomes invalid.
    """

    url: str
    expires_at: datetime | None = None
