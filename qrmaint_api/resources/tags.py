"""Resource class for the Tags endpoint (/tags)."""

from ..models.common import PaginatedResponse
from ..models.tags import Tag, TagType
from .base import BaseResource


class TagsResource(BaseResource):
    """Provides read operations for QrMaint tags.

    Access via ``client.tags``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
        tag_type: TagType | None = None,
    ) -> PaginatedResponse[Tag]:
        """Return a paginated list of tags.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to tag name.
            tag_type: Filter to tags associated with this resource category
                (see :class:`~qrmaint_api.models.tags.TagType`).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.tags.Tag` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "type": tag_type.value if tag_type else None,
        })
        return self._parse_paginated(self._get("/tags", params=params), Tag)
