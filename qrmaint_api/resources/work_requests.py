"""Resource class for the Work Requests endpoint (/work-requests)."""
from __future__ import annotations

from ..models.common import CreatedObject, PaginatedResponse
from ..models.work_requests import WorkRequest, WorkRequestParams
from .base import BaseResource


class WorkRequestsResource(BaseResource):
    """Provides read and create operations for QrMaint work requests.

    Access via ``client.work_requests``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[WorkRequest]:
        """Return a paginated list of work requests.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to request subject and number.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.work_requests.WorkRequest` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        return self._parse_paginated(self._get("/work-requests", params=params), WorkRequest)

    def get(self, request_id: int) -> WorkRequest:
        """Fetch a single work request by its internal ID.

        Args:
            request_id: Internal integer ID of the work request.

        Returns:
            The matching :class:`~qrmaint_api.models.work_requests.WorkRequest`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no work request matches the given ID.
        """
        return self._parse_single(self._get(f"/work-requests/{request_id}"), WorkRequest)

    def create(self, params: WorkRequestParams) -> CreatedObject:
        """Submit a new work request.

        Args:
            params: Field values for the new work request.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new work request's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/work-requests", json=body), CreatedObject)
