"""Resource class for the Parts endpoint (/parts)."""

from ..models.common import CreatedObject, PaginatedResponse
from ..models.parts import Part, PartParams
from .base import BaseResource


class PartsResource(BaseResource):
    """Provides operations for QrMaint spare parts.

    Access via ``client.parts``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
        location_id: int | None = None,
    ) -> PaginatedResponse[Part]:
        """Return a paginated list of parts.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to part name and number.
            location_id: Filter to parts associated with this location.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.parts.Part` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "locationId": location_id,
        })
        return self._parse_paginated(self._get("/parts", params=params), Part)

    def create(self, params: PartParams) -> CreatedObject:
        """Create a new part.

        Args:
            params: Field values for the new part.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new part's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/parts", json=body), CreatedObject)
