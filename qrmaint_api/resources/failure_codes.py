"""Resource class for the Failure Codes endpoint (/failure-codes)."""
from __future__ import annotations

from ..models.common import PaginatedResponse
from ..models.failure_codes import FailureCode
from .base import BaseResource


class FailureCodesResource(BaseResource):
    """Provides read operations for QrMaint failure codes.

    Access via ``client.failure_codes``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[FailureCode]:
        """Return a paginated list of failure codes.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to failure code name.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.failure_codes.FailureCode` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        return self._parse_paginated(self._get("/failure-codes", params=params), FailureCode)
