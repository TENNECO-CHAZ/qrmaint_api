"""Resource class for the Assets endpoint (/assets)."""

from ..models.assets import Asset, AssetParams, AssetPlannedProductionTime, UpdatedAssetParams
from ..models.common import CreatedObject, IdType, PaginatedResponse, UpdatedObject
from .base import BaseResource


class AssetsResource(BaseResource):
    """Provides CRUD operations for QrMaint assets.

    Access via ``client.assets``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
        parent_id: int | None = None,
        parent_external_id: str | None = None,
        location_id: int | None = None,
        location_external_id: str | None = None,
        tag_ids: list[int] | None = None,
    ) -> PaginatedResponse[Asset]:
        """Return a paginated list of assets.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search string applied to asset name and number.
            parent_id: Filter to nested assets under this parent asset ID.
            parent_external_id: Filter by external ID of the parent asset.
            location_id: Filter to assets at this location.
            location_external_id: Filter by external ID of the location.
            tag_ids: Filter to assets tagged with any of these tag IDs.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.assets.Asset` objects.
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
        return self._parse_paginated(self._get("/assets", params=params), Asset)

    def get(self, asset_id: int, *, id_type: IdType = IdType.ID) -> Asset:
        """Fetch a single asset by its identifier.

        Args:
            asset_id: The asset identifier (internal ID or external ID depending
                on *id_type*).
            id_type: Whether *asset_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            The matching :class:`~qrmaint_api.models.assets.Asset`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no asset matches the given ID.
        """
        params = self._clean_params({"usedIdType": id_type.value})
        return self._parse_single(self._get(f"/assets/{asset_id}", params=params), Asset)

    def create(self, params: AssetParams) -> CreatedObject:
        """Create a new asset.

        Args:
            params: Field values for the new asset.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new asset's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/assets", json=body), CreatedObject)

    def update(self, asset_id: int, params: UpdatedAssetParams, *, id_type: IdType = IdType.ID) -> UpdatedObject:
        """Partially update an existing asset.

        Args:
            asset_id: The asset identifier.
            params: Fields to update; omitted fields are left unchanged.
            id_type: Whether *asset_id* is an internal or external identifier.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no asset matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        body["usedIdType"] = id_type.value
        return self._parse_single(self._put(f"/assets/{asset_id}", json=body), UpdatedObject)

    def get_planned_production_time(self, asset_id: int) -> AssetPlannedProductionTime:
        """Fetch the planned production time configuration for an asset.

        Args:
            asset_id: Internal integer ID of the asset.

        Returns:
            An :class:`~qrmaint_api.models.assets.AssetPlannedProductionTime`
            with the daily production time values.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no asset matches the given ID.
        """
        data = self._get(f"/assets/{asset_id}/planned-production-time")
        return self._parse_single(data, AssetPlannedProductionTime)
