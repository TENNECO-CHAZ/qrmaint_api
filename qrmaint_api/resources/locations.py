"""Resource class for the Locations endpoint (/locations)."""
from __future__ import annotations

from ..models.common import CreatedObject, IdType, PaginatedResponse, UpdatedObject
from ..models.locations import Location, LocationParams, UpdatedLocationParams
from .base import BaseResource


class LocationsResource(BaseResource):
    """Provides CRUD operations for QrMaint locations.

    Access via ``client.locations``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
        parent_id: int | None = None,
        parent_external_id: str | None = None,
        type_id: int | None = None,
    ) -> PaginatedResponse[Location]:
        """Return a paginated list of locations.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search string applied to location name.
            parent_id: Filter to direct children of this parent location.
            parent_external_id: Filter by external ID of the parent location.
            type_id: Filter to locations of this dictionary type.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.locations.Location` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "parentId": parent_id,
            "parentExternalId": parent_external_id,
            "typeId": type_id,
        })
        return self._parse_paginated(self._get("/locations", params=params), Location)

    def get(self, location_id: int, *, id_type: IdType = IdType.ID) -> Location:
        """Fetch a single location by its identifier.

        Args:
            location_id: The location identifier.
            id_type: Whether *location_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            The matching :class:`~qrmaint_api.models.locations.Location`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no location matches the given ID.
        """
        params = self._clean_params({"usedIdType": id_type.value})
        return self._parse_single(self._get(f"/locations/{location_id}", params=params), Location)

    def create(self, params: LocationParams) -> CreatedObject:
        """Create a new location.

        Args:
            params: Field values for the new location.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new location's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/locations", json=body), CreatedObject)

    def update(self, location_id: int, params: UpdatedLocationParams, *, id_type: IdType = IdType.ID) -> UpdatedObject:
        """Partially update an existing location.

        Args:
            location_id: The location identifier.
            params: Fields to update; omitted fields are left unchanged.
            id_type: Whether *location_id* is an internal or external identifier.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no location matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        body["usedIdType"] = id_type.value
        return self._parse_single(self._put(f"/locations/{location_id}", json=body), UpdatedObject)
