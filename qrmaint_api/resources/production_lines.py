"""Resource class for the Production Lines endpoint (/production-lines)."""
from __future__ import annotations

from ..models.common import CreatedObject, IdType, PaginatedResponse, UpdatedObject
from ..models.production_lines import ProductionLine, ProductionLineParams, UpdatedProductionLineParams
from .base import BaseResource


class ProductionLinesResource(BaseResource):
    """Provides CRUD operations for QrMaint production lines.

    Access via ``client.production_lines``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 100,
        query: str | None = None,
        parent_id: int | None = None,
        parent_external_id: str | None = None,
        location_id: int | None = None,
        location_external_id: str | None = None,
        tag_ids: list[int] | None = None,
    ) -> PaginatedResponse[ProductionLine]:
        """Return a paginated list of production lines.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to line name.
            parent_id: Filter to lines whose parent asset has this internal ID.
            parent_external_id: Filter by external ID of the parent asset.
            location_id: Filter to lines at this location.
            location_external_id: Filter by external ID of the location.
            tag_ids: Filter to lines tagged with any of these tag IDs.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.production_lines.ProductionLine` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "parentId": parent_id,
            "parentExternalId": parent_external_id,
            "locationId": location_id,
            "locationExternalId": location_external_id,
            "tagIds": tag_ids,
        })
        return self._parse_paginated(self._get("/production-lines", params=params), ProductionLine)

    def get(self, line_id: int, *, id_type: IdType = IdType.ID) -> ProductionLine:
        """Fetch a single production line by its identifier.

        Args:
            line_id: The line identifier.
            id_type: Whether *line_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            The matching :class:`~qrmaint_api.models.production_lines.ProductionLine`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no line matches the given ID.
        """
        params = self._clean_params({"usedIdType": id_type.value})
        return self._parse_single(self._get(f"/production-lines/{line_id}", params=params), ProductionLine)

    def create(self, params: ProductionLineParams) -> CreatedObject:
        """Create a new production line.

        Args:
            params: Field values for the new line.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new line's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/production-lines", json=body), CreatedObject)

    def update(self, line_id: int, params: UpdatedProductionLineParams, *, id_type: IdType = IdType.ID) -> UpdatedObject:
        """Partially update an existing production line.

        Args:
            line_id: The line identifier.
            params: Fields to update; omitted fields are left unchanged.
            id_type: Whether *line_id* is an internal or external identifier.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no line matches the given ID.
        """
        query = self._clean_params({"usedIdType": id_type.value})
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put(f"/production-lines/{line_id}", json=body, params=query), UpdatedObject)
