"""Resource class for the Production Areas endpoint (/production-areas)."""

from ..models.common import CreatedObject, IdType, PaginatedResponse, UpdatedObject
from ..models.production_areas import ProductionArea, ProductionAreaParams, UpdatedProductionAreaParams
from .base import BaseResource


class ProductionAreasResource(BaseResource):
    """Provides CRUD operations for QrMaint production areas.

    Access via ``client.production_areas``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 100,
        query: str | None = None,
        parent_id: int | None = None,
        parent_external_id: str | None = None,
        type_id: int | None = None,
    ) -> PaginatedResponse[ProductionArea]:
        """Return a paginated list of production areas.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to area name.
            parent_id: Filter to direct children of this parent area/location.
            parent_external_id: Filter by external ID of the parent instead of
                internal ID.
            type_id: Filter to areas of this dictionary type.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.production_areas.ProductionArea` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "parentId": parent_id,
            "parentExternalId": parent_external_id,
            "typeId": type_id,
        })
        return self._parse_paginated(self._get("/production-areas", params=params), ProductionArea)

    def get(self, area_id: int, *, id_type: IdType = IdType.ID) -> ProductionArea:
        """Fetch a single production area by its identifier.

        Args:
            area_id: The area identifier.
            id_type: Whether *area_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            The matching :class:`~qrmaint_api.models.production_areas.ProductionArea`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no area matches the given ID.
        """
        params = self._clean_params({"usedIdType": id_type.value})
        return self._parse_single(self._get(f"/production-areas/{area_id}", params=params), ProductionArea)

    def create(self, params: ProductionAreaParams) -> CreatedObject:
        """Create a new production area.

        Args:
            params: Field values for the new area.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new area's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/production-areas", json=body), CreatedObject)

    def update(self, area_id: int, params: UpdatedProductionAreaParams, *, id_type: IdType = IdType.ID) -> UpdatedObject:
        """Partially update an existing production area.

        Args:
            area_id: The area identifier.
            params: Fields to update; omitted fields are left unchanged.
            id_type: Whether *area_id* is an internal or external identifier.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no area matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        body["usedIdType"] = id_type.value
        return self._parse_single(self._put(f"/production-areas/{area_id}", json=body), UpdatedObject)
