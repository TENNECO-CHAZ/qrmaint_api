"""Resource class for the Andon Calls endpoint (/andon-calls)."""
from __future__ import annotations

from ..models.andon_calls import AndonCall, AndonCallType
from ..models.common import PaginatedResponse
from .base import BaseResource


class AndonCallsResource(BaseResource):
    """Provides read operations for QrMaint Andon call records.

    Access via ``client.andon_calls``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        asset_id: int | None = None,
        status: str | None = None,
    ) -> PaginatedResponse[AndonCall]:
        """Return a paginated list of Andon calls.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            asset_id: Filter to calls triggered on this asset.
            status: Filter by call status string (e.g. ``"OPEN"``, ``"CLOSED"``).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.andon_calls.AndonCall` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "assetId": asset_id,
            "status": status,
        })
        return self._parse_paginated(self._get("/andon-calls", params=params), AndonCall)

    def list_types(self) -> list[AndonCallType]:
        """Return all configured Andon call types (non-paginated).

        Returns:
            A list of :class:`~qrmaint_api.models.andon_calls.AndonCallType`
            objects describing the available call categories.
        """
        data = self._get("/andon-calls/types")
        return [AndonCallType.model_validate(item) for item in data]
