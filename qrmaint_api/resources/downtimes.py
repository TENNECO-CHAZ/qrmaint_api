"""Resource class for the Downtimes endpoint (/downtimes)."""
from __future__ import annotations

from datetime import datetime

from ..models.common import CreatedObject, PaginatedResponse
from ..models.downtimes import Downtime, DowntimeParams
from .base import BaseResource


class DowntimesResource(BaseResource):
    """Provides operations for QrMaint asset downtime records.

    Access via ``client.downtimes``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        asset_or_location_id: int | None = None,
        asset_or_location_external_id: str | None = None,
        get_nested: bool | None = None,
        only_active: bool | None = None,
        datetime_from: datetime | None = None,
        datetime_to: datetime | None = None,
        work_id: int | None = None,
    ) -> PaginatedResponse[Downtime]:
        """Return a paginated list of downtime records.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            asset_or_location_id: Filter to downtimes for this asset or location.
            asset_or_location_external_id: Filter by asset or location external ID.
            get_nested: Include downtimes for all nested children of the given node.
            only_active: Return only currently active (open) downtimes.
            datetime_from: Return downtimes starting on or after this timestamp.
            datetime_to: Return downtimes starting before or on this timestamp.
            work_id: Filter to downtimes linked to this work order.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.downtimes.Downtime` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "assetOrLocationId": asset_or_location_id,
            "assetOrLocationExternalId": asset_or_location_external_id,
            "getNested": get_nested,
            "onlyActive": only_active,
            "datetimeFrom": datetime_from.isoformat() if datetime_from else None,
            "datetimeTo": datetime_to.isoformat() if datetime_to else None,
            "workId": work_id,
        })
        return self._parse_paginated(self._get("/downtimes", params=params), Downtime)

    def get(self, downtime_id: int) -> Downtime:
        """Fetch a single downtime record by its internal ID.

        Args:
            downtime_id: Internal integer ID of the downtime record.

        Returns:
            The matching :class:`~qrmaint_api.models.downtimes.Downtime`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no downtime matches the given ID.
        """
        return self._parse_single(self._get(f"/downtimes/{downtime_id}"), Downtime)

    def create(self, params: DowntimeParams) -> CreatedObject:
        """Record a new downtime event.

        Args:
            params: Field values for the new downtime record.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new downtime's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/downtimes", json=body), CreatedObject)
