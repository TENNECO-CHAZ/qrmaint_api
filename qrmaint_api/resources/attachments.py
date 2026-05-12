"""Resource class for the Attachments endpoint (/attachments)."""
from __future__ import annotations

from ..models.attachments import Attachment, AttachmentDownloadUrl
from ..models.common import PaginatedResponse
from .base import BaseResource


class AttachmentsResource(BaseResource):
    """Provides read operations for QrMaint file attachments.

    Access via ``client.attachments``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[Attachment]:
        """Return a paginated list of attachments.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Filter by file name or type group.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.attachments.Attachment` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        return self._parse_paginated(self._get("/attachments", params=params), Attachment)

    def get(self, attachment_id: int) -> Attachment:
        """Fetch a single attachment record by its internal ID.

        Args:
            attachment_id: Internal integer ID of the attachment.

        Returns:
            The matching :class:`~qrmaint_api.models.attachments.Attachment`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no attachment matches the given ID.
        """
        return self._parse_single(self._get(f"/attachments/{attachment_id}"), Attachment)

    def get_download_url(self, attachment_id: int) -> AttachmentDownloadUrl:
        """Obtain a time-limited pre-signed URL to download an attachment.

        Args:
            attachment_id: Internal integer ID of the attachment.

        Returns:
            An :class:`~qrmaint_api.models.attachments.AttachmentDownloadUrl`
            with the URL and its expiry timestamp.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no attachment matches the given ID.
        """
        return self._parse_single(self._get(f"/attachments/{attachment_id}/download-url"), AttachmentDownloadUrl)
