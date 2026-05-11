"""Resource class for the Shifts endpoint (/shifts)."""

from ..models.common import PaginatedResponse
from ..models.shifts import Shift
from .base import BaseResource


class ShiftsResource(BaseResource):
    """Provides read operations for QrMaint work shifts.

    Access via ``client.shifts``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[Shift]:
        """Return a paginated list of shifts.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to shift name.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.shifts.Shift` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        return self._parse_paginated(self._get("/shifts", params=params), Shift)
