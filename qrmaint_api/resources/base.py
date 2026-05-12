"""Abstract base class shared by all resource helpers."""
from __future__ import annotations


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
