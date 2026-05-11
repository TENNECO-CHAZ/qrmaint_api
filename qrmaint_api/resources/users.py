"""Resource class for the Users endpoint (/users)."""
from __future__ import annotations

from ..models.common import PaginatedResponse
from ..models.users import User
from .base import BaseResource


class UsersResource(BaseResource):
    """Provides read operations for QrMaint platform users.

    Access via ``client.users``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[User]:
        """Return a paginated list of users.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to user name and email.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.users.User` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        return self._parse_paginated(self._get("/users", params=params), User)
