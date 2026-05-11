"""Resource class for the Teams endpoint (/teams)."""

from ..models.common import PaginatedResponse
from ..models.teams import Team
from .base import BaseResource


class TeamsResource(BaseResource):
    """Provides read operations for QrMaint teams.

    Access via ``client.teams``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[Team]:
        """Return a paginated list of teams.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to team name.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.teams.Team` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        return self._parse_paginated(self._get("/teams", params=params), Team)
