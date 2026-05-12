"""Resource class for the Andon Calls endpoint (/andon-calls)."""
from __future__ import annotations

from ..models.andon_calls import AndonCall
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
        only_active: bool | None = None,
        asset_or_location_id: int | None = None,
        asset_or_location_external_id: str | None = None,
        priority: int | None = None,
        query: str | None = None,
        teams_ids: list[int] | None = None,
    ) -> PaginatedResponse[AndonCall]:
        """Return a paginated list of Andon calls.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            only_active: Filter to active calls only.
            asset_or_location_id: Filter to calls for this asset or location ID.
            asset_or_location_external_id: Filter by asset or location external ID.
            priority: Filter by priority value.
            query: Filter by call type name.
            teams_ids: Filter to calls assigned to any of these team IDs.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.andon_calls.AndonCall` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "onlyActive": only_active,
            "assetOrLocationId": asset_or_location_id,
            "assetOrLocationExternalId": asset_or_location_external_id,
            "priority": priority,
            "query": query,
            "teamsIds": teams_ids,
        })
        return self._parse_paginated(self._get("/andon-calls", params=params), AndonCall)

    def list_types(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        asset_or_location_id: int | None = None,
        asset_or_location_external_id: str | None = None,
        priority: int | None = None,
        team_id: int | None = None,
        andon_panel_user_id: int | None = None,
        query: str | None = None,
    ) -> PaginatedResponse[AndonCall]:
        """Return a paginated list of Andon call types.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            asset_or_location_id: Filter by asset or location ID.
            asset_or_location_external_id: Filter by asset or location external ID.
            priority: Filter by priority value.
            team_id: Filter by team ID.
            andon_panel_user_id: Filter by ANDON panel user ID.
            query: Filter by call type name or team name.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.andon_calls.AndonCall` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "assetOrLocationId": asset_or_location_id,
            "assetOrLocationExternalId": asset_or_location_external_id,
            "priority": priority,
            "teamId": team_id,
            "andonPanelUserId": andon_panel_user_id,
            "query": query,
        })
        return self._parse_paginated(self._get("/andon-calls/types", params=params), AndonCall)
