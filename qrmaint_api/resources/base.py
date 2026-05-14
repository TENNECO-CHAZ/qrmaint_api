"""Abstract base class shared by all resource helpers."""
from __future__ import annotations

import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING, Any, TypeVar, Type

from ..models.common import PaginatedResponse, _CamelModel

if TYPE_CHECKING:
    from ..client import QrMaintClient

T = TypeVar("T", bound=_CamelModel)


class BaseResource:
    """Provides common HTTP helpers and response-parsing utilities.

    Every domain resource (assets, locations, work orders, …) extends this
    class and gains a reference to the singleton ``QrMaintClient``, thin
    wrappers around each HTTP verb, and type-safe response parsers.

    Attributes:
        _client: The shared ``QrMaintClient`` instance used to issue requests
            and apply rate limiting.
    """

    def __init__(self, client: QrMaintClient) -> None:
        """Store a reference to the shared API client.

        Args:
            client: The singleton ``QrMaintClient`` that owns this resource.
        """
        self._client = client

    # ------------------------------------------------------------------
    # HTTP verb helpers
    # ------------------------------------------------------------------

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        """Issue a GET request and return the unwrapped payload dict.

        Args:
            path: API path relative to the base URL (e.g. ``"/assets"``).
            params: Optional query-string parameters.

        Returns:
            The ``payload`` value from the API response envelope.
        """
        return self._client._request("GET", path, params=params)

    def _post(self, path: str, json: dict | None = None, params: dict | None = None) -> dict:
        """Issue a POST request and return the unwrapped payload dict.

        Args:
            path: API path relative to the base URL.
            json: Request body serialised as JSON.
            params: Optional query-string parameters.

        Returns:
            The ``payload`` value from the API response envelope.
        """
        return self._client._request("POST", path, json=json, params=params)

    def _put(self, path: str, json: dict | None = None, params: dict | None = None) -> dict:
        """Issue a PUT request and return the unwrapped payload dict.

        Args:
            path: API path relative to the base URL.
            json: Request body serialised as JSON.
            params: Optional query-string parameters.

        Returns:
            The ``payload`` value from the API response envelope.
        """
        return self._client._request("PUT", path, json=json, params=params)

    def _patch(self, path: str, json: dict | None = None, params: dict | None = None) -> dict:
        """Issue a PATCH request and return the unwrapped payload dict.

        Args:
            path: API path relative to the base URL.
            json: Partial request body serialised as JSON.
            params: Optional query-string parameters.

        Returns:
            The ``payload`` value from the API response envelope.
        """
        return self._client._request("PATCH", path, json=json, params=params)

    def _delete(self, path: str) -> dict:
        """Issue a DELETE request and return the unwrapped payload dict.

        Args:
            path: API path relative to the base URL.

        Returns:
            The ``payload`` value from the API response envelope.
        """
        return self._client._request("DELETE", path)

    # ------------------------------------------------------------------
    # Response parsers
    # ------------------------------------------------------------------

    def _parse_paginated(self, data: dict, model: Type[T]) -> PaginatedResponse[T]:
        """Deserialise a paginated list response into a typed ``PaginatedResponse``.

        Args:
            data: Raw dict from the API (already unwrapped from the envelope).
            model: The Pydantic model class used to parse each item in ``data``.

        Returns:
            A ``PaginatedResponse[model]`` instance with typed ``data`` items.
        """
        return PaginatedResponse[model].model_validate(data)

    def _parse_single(self, data: dict, model: Type[T]) -> T:
        """Deserialise a single-object response into the given Pydantic model.

        Args:
            data: Raw dict from the API (already unwrapped from the envelope).
            model: The Pydantic model class to instantiate.

        Returns:
            A validated instance of ``model``.
        """
        return model.model_validate(data)

    def _clean_params(self, params: dict[str, Any]) -> dict[str, Any]:
        """Remove ``None`` values from a query-parameter dict.

        Keeps the request URL clean by omitting parameters that were not
        explicitly supplied by the caller.

        Args:
            params: Raw parameter dict possibly containing ``None`` values.

        Returns:
            A new dict with all ``None`` entries removed.
        """
        return {k: v for k, v in params.items() if v is not None}

    def _fetch_all_pages(
        self,
        path: str,
        model: Type[T],
        params: dict[str, Any] | None = None,
        per_page: int = 100,
        max_workers: int = 10,
    ) -> list[T]:
        """Fetch every page of a paginated endpoint and return a flat list.

        Issues page 1 first to discover the total record count, then fires
        all remaining pages concurrently up to *max_workers* threads.  The
        rate limiter serialises slot acquisition, so throughput never exceeds
        the API's 10 req/s window while network I/O is fully parallelised.

        Args:
            path: API path relative to the base URL (e.g. ``"/parts"``).
            model: Pydantic model class for each item in the response.
            params: Extra query-string parameters (must not include ``page``
                or ``perPage``; those are managed internally).
            per_page: Page size sent to the API (max 100).
            max_workers: Maximum parallel worker threads (default 10).

        Returns:
            All items across every page, in page order.
        """
        base = {**(params or {}), "perPage": per_page}

        first = self._parse_paginated(self._get(path, params={**base, "page": 1}), model)
        result: list[T] = list(first.data)
        total_pages = math.ceil(first.all_records_count / per_page) if first.all_records_count else 1

        if total_pages <= 1:
            return result

        def _fetch(page: int) -> tuple[int, list]:
            data = self._parse_paginated(self._get(path, params={**base, "page": page}), model).data
            return page, data

        pages: dict[int, list] = {}
        workers = min(max_workers, total_pages - 1)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(_fetch, p): p for p in range(2, total_pages + 1)}
            for future in as_completed(futures):
                page_num, data = future.result()
                pages[page_num] = data

        for p in range(2, total_pages + 1):
            result.extend(pages[p])

        return result
