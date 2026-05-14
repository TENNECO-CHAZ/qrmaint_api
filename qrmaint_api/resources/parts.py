"""Resource class for the Parts endpoint (/parts)."""
from __future__ import annotations

from datetime import datetime

from ..models.common import CreatedObject, IdType, PaginatedResponse, UpdatedObject
from ..models.parts import Part, PartParams, PartSupplier, PartSupplierParams, PartSupplierUpdateParams, PartUpdateParams
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
        type_id: int | None = None,
        inventory_id: int | None = None,
        only_critical: bool | None = None,
        created_datetime_from: datetime | str | None = None,
        created_datetime_to: datetime | str | None = None,
        modified_datetime_from: datetime | str | None = None,
        modified_datetime_to: datetime | str | None = None,
    ) -> PaginatedResponse[Part]:
        """Return a paginated list of parts.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to part name and number.
            type_id: Filter to parts belonging to this part type.
            inventory_id: Filter to parts associated with this inventory.
            only_critical: When ``True``, return only critical parts.
            created_datetime_from: Include only parts created on or after this datetime (ISO 8601).
            created_datetime_to: Include only parts created on or before this datetime (ISO 8601).
            modified_datetime_from: Include only parts modified on or after this datetime (ISO 8601).
            modified_datetime_to: Include only parts modified on or before this datetime (ISO 8601).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.parts.Part` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "typeId": type_id,
            "inventoryId": inventory_id,
            "onlyCritical": only_critical,
            "createdDatetimeFrom": created_datetime_from,
            "createdDatetimeTo": created_datetime_to,
            "modifiedDatetimeFrom": modified_datetime_from,
            "modifiedDatetimeTo": modified_datetime_to,
        })
        return self._parse_paginated(self._get("/parts", params=params), Part)

    def get(self, part_id: int | str, *, id_type: IdType = IdType.ID) -> Part:
        """Fetch a single part by its identifier.

        Args:
            part_id: The part identifier (internal ID or external ID depending
                on *id_type*).
            id_type: Whether *part_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            The matching :class:`~qrmaint_api.models.parts.Part`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no part matches the given ID.
        """
        params = self._clean_params({"usedIdType": id_type.value})
        return self._parse_single(self._get(f"/parts/{part_id}", params=params), Part)

    def list_suppliers(
        self,
        part_id: int | str,
        *,
        id_type: IdType = IdType.ID,
        query: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> PaginatedResponse[PartSupplier]:
        """Return a paginated list of suppliers for a part.

        Args:
            part_id: The part identifier (internal ID or external ID depending
                on *id_type*).
            id_type: Whether *part_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.
            query: Free-text search applied to supplier name and part number.
            page: 1-based page number.
            per_page: Number of records per page (max 100).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.parts.PartSupplier` objects.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no part matches the given ID.
        """
        params = self._clean_params({
            "usedPartIdType": id_type.value,
            "query": query,
            "page": page,
            "perPage": per_page,
        })
        return self._parse_paginated(
            self._get(f"/parts/{part_id}/suppliers", params=params), PartSupplier
        )

    def add_supplier(
        self,
        part_id: int | str,
        params: PartSupplierParams,
        *,
        id_type: IdType = IdType.ID,
    ) -> CreatedObject:
        """Add a supplier to a part.

        Args:
            part_id: The part identifier (internal ID or external ID depending
                on *id_type*).
            params: Supplier fields to associate with the part.
            id_type: Whether *part_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new association's ``id``.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no part matches the given ID.
        """
        query = self._clean_params({"usedPartIdType": id_type.value})
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(
            self._post(f"/parts/{part_id}/suppliers", json=body, params=query), CreatedObject
        )

    def update_supplier(
        self,
        part_id: int | str,
        supplier_id: int,
        params: PartSupplierUpdateParams,
        *,
        id_type: IdType = IdType.ID,
    ) -> UpdatedObject:
        """Update a supplier associated with a part.

        Args:
            part_id: The part identifier (internal ID or external ID depending
                on *id_type*).
            supplier_id: Internal ID of the supplier to update.
            params: Fields to update on the supplier association.
            id_type: Whether *part_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` containing the
            association's ``id``.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no part or supplier matches
                the given IDs.
        """
        query = self._clean_params({"usedPartIdType": id_type.value})
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(
            self._patch(f"/parts/{part_id}/suppliers/{supplier_id}", json=body, params=query),
            UpdatedObject,
        )

    def update(self, part_id: int | str, params: PartUpdateParams, *, id_type: IdType = IdType.ID) -> UpdatedObject:
        """Update an existing part.

        Args:
            part_id: The part identifier (internal ID or external ID depending
                on *id_type*).
            params: Fields to update; omitted fields are left unchanged.
            id_type: Whether *part_id* is an internal :attr:`IdType.ID` or an
                :attr:`IdType.EXTERNAL_ID`.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` containing the
            updated part's ``id``.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no part matches the given ID.
        """
        query = self._clean_params({"usedIdType": id_type.value})
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put(f"/parts/{part_id}", json=body, params=query), UpdatedObject)

    def list_all(
        self,
        *,
        query: str | None = None,
        type_id: int | None = None,
        inventory_id: int | None = None,
        only_critical: bool | None = None,
        created_datetime_from: datetime | str | None = None,
        created_datetime_to: datetime | str | None = None,
        modified_datetime_from: datetime | str | None = None,
        modified_datetime_to: datetime | str | None = None,
        max_workers: int = 10,
    ) -> list[Part]:
        """Fetch every part across all pages using parallel requests.

        Equivalent to calling :meth:`list` repeatedly for every page, but
        fires up to *max_workers* pages concurrently so the full collection
        is retrieved in a fraction of the sequential time.

        Args:
            query: Free-text search applied to part name and number.
            type_id: Filter to parts belonging to this part type.
            inventory_id: Filter to parts associated with this inventory.
            only_critical: When ``True``, return only critical parts.
            created_datetime_from: Include only parts created on or after
                this datetime (ISO 8601 string or ``datetime`` object).
            created_datetime_to: Include only parts created on or before
                this datetime.
            modified_datetime_from: Include only parts modified on or after
                this datetime.
            modified_datetime_to: Include only parts modified on or before
                this datetime.
            max_workers: Maximum parallel worker threads (default 10,
                matching the API's per-second rate limit).

        Returns:
            A flat list of every :class:`~qrmaint_api.models.parts.Part`
            matching the filters, in page order.
        """
        params = self._clean_params({
            "query": query,
            "typeId": type_id,
            "inventoryId": inventory_id,
            "onlyCritical": only_critical,
            "createdDatetimeFrom": created_datetime_from,
            "createdDatetimeTo": created_datetime_to,
            "modifiedDatetimeFrom": modified_datetime_from,
            "modifiedDatetimeTo": modified_datetime_to,
        })
        return self._fetch_all_pages("/parts", Part, params=params, max_workers=max_workers)

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
