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
        asset_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> PaginatedResponse[Downtime]:
        """Return a paginated list of downtime records.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            asset_id: Filter to downtimes for this asset.
            start_date: Return only downtimes that started on or after this UTC
                timestamp.
            end_date: Return only downtimes that started before or on this UTC
                timestamp.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.downtimes.Downtime` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "assetId": asset_id,
            "startDate": start_date.isoformat() if start_date else None,
            "endDate": end_date.isoformat() if end_date else None,
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
