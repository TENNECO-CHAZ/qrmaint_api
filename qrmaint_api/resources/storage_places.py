"""Resource class for the Storage Places endpoint (/dictionaries/storage-places)."""
from __future__ import annotations

from ..models.common import CreatedObject, IdType, PaginatedResponse, UpdatedObject
from ..models.storage_places import StoragePlace, StoragePlaceParams, UpdatedStoragePlaceParams
from .base import BaseResource


class StoragePlacesResource(BaseResource):
    """Provides CRUD operations for QrMaint storage places (warehouse locations).

    Access via ``client.storage_places``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
        warehouse_id: int | None = None,
        parent_id: int | None = None,
    ) -> PaginatedResponse[StoragePlace]:
        """Return a paginated list of storage places.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to storage place name.
            warehouse_id: Filter to locations within this warehouse.
            parent_id: Filter to direct children of this parent storage place.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.storage_places.StoragePlace` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "warehouseId": warehouse_id,
            "parentId": parent_id,
        })
        return self._parse_paginated(self._get("/dictionaries/storage-places", params=params), StoragePlace)

    def get(self, storage_place_id: int, *, id_type: IdType = IdType.ID) -> StoragePlace:
        """Fetch a single storage place by its identifier.

        Args:
            storage_place_id: The storage place identifier.
            id_type: Whether *storage_place_id* is an internal :attr:`IdType.ID`
                or an :attr:`IdType.EXTERNAL_ID`.

        Returns:
            The matching :class:`~qrmaint_api.models.storage_places.StoragePlace`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no storage place matches the given ID.
        """
        params = self._clean_params({"usedIdType": id_type.value})
        return self._parse_single(
            self._get(f"/dictionaries/storage-places/{storage_place_id}", params=params),
            StoragePlace,
        )

    def create(self, params: StoragePlaceParams) -> CreatedObject:
        """Create a new storage place.

        Args:
            params: Field values for the new storage place, including the
                required *warehouse_id*.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new storage place's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/dictionaries/storage-places", json=body), CreatedObject)

    def update(self, storage_place_id: int, params: UpdatedStoragePlaceParams, *, id_type: IdType = IdType.ID) -> UpdatedObject:
        """Partially update an existing storage place.

        Args:
            storage_place_id: The storage place identifier.
            params: Fields to update; omitted fields are left unchanged.
            id_type: Whether *storage_place_id* is an internal or external
                identifier.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no storage place matches the given ID.
        """
        query = self._clean_params({"usedIdType": id_type.value})
        body = params.model_dump(by_alias=True, exclude_none=True)
        path = f"/dictionaries/storage-places/{storage_place_id}"
        return self._parse_single(self._patch(path, json=body, params=query), UpdatedObject)
