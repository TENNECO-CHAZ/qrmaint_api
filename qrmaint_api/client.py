"""Singleton HTTP client for the QrMaint REST API.

Typical usage::

    from qrmaint_api import QrMaintClient

    client = QrMaintClient(api_token="your-token")
    # or set the QRMAINT_API_TOKEN environment variable and call QrMaintClient()

    assets = client.assets.list(page=1, per_page=100)
    for asset in assets.data:
        print(asset.id, asset.name)
"""
from __future__ import annotations


import os
import threading
from typing import Any

import httpx

from ._rate_limiter import RateLimiter
from .exceptions import APIError, AuthenticationError, NotFoundError, RateLimitError
from .resources.andon_calls import AndonCallsResource
from .resources.assets import AssetsResource
from .resources.attachments import AttachmentsResource
from .resources.dictionaries import DictionariesResource
from .resources.downtimes import DowntimesResource
from .resources.failure_codes import FailureCodesResource
from .resources.inventory import InventoryResource
from .resources.locations import LocationsResource
from .resources.parts import PartsResource
from .resources.production_areas import ProductionAreasResource
from .resources.production_lines import ProductionLinesResource
from .resources.purchase_requests import PurchaseRequestsResource
from .resources.shifts import ShiftsResource
from .resources.stocks import StocksResource
from .resources.storage_places import StoragePlacesResource
from .resources.tags import TagsResource
from .resources.teams import TeamsResource
from .resources.users import UsersResource
from .resources.vendors import VendorsResource
from .resources.work_orders import WorkOrdersResource
from .resources.work_requests import WorkRequestsResource

_BASE_URL = "https://api.qrmaint.com/v1"


class QrMaintClient:
    """Singleton HTTP client for the QrMaint REST API.

    Only one instance is ever created per process.  The first call to the
    constructor initialises the client (HTTP session, rate limiter, resource
    objects); subsequent calls with any arguments simply return the existing
    instance unchanged.

    The API token can be supplied either as a constructor argument or via the
    ``QRMAINT_API_TOKEN`` environment variable.

    All domain operations are exposed through typed resource attributes:

    - ``assets`` – physical assets
    - ``locations`` – physical locations
    - ``production_areas`` – production area nodes
    - ``production_lines`` – production line nodes
    - ``downtimes`` – asset downtime records
    - ``failure_codes`` – failure codes
    - ``parts`` – spare parts / inventory items
    - ``andon_calls`` – andon (alert) calls
    - ``inventory`` – inventory documents and stock adjustments
    - ``attachments`` – file attachments
    - ``dictionaries`` – configurable dictionary items
    - ``purchase_requests`` – purchase requests
    - ``shifts`` – work shifts
    - ``stocks`` – stock levels and logs
    - ``storage_places`` – warehouse storage places
    - ``tags`` – classification tags
    - ``teams`` – user teams
    - ``users`` – platform users
    - ``vendors`` – vendors / suppliers
    - ``work_orders`` – maintenance work orders
    - ``work_requests`` – maintenance work requests

    Example::

        client = QrMaintClient(api_token="ey...")
        wo = client.work_orders.get(12345)
        print(wo.title, wo.status_name)
    """

    _instance: QrMaintClient | None = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, api_token: str | None = None) -> QrMaintClient:
        """Return the singleton instance, creating it on the first call.

        Args:
            api_token: Ignored after the first instantiation.

        Returns:
            The single shared ``QrMaintClient`` instance.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_token: str | None = None) -> None:
        """Initialise the client on first call; no-op on subsequent calls.

        Args:
            api_token: Bearer token generated in the QrMaint app settings.
                If ``None``, the ``QRMAINT_API_TOKEN`` environment variable
                is used instead.

        Raises:
            ValueError: If no token is provided and ``QRMAINT_API_TOKEN`` is
                not set.
        """
        if hasattr(self, "_initialized"):
            return

        token = api_token or os.environ.get("QRMAINT_API_TOKEN")
        if not token:
            raise ValueError("api_token is required or set QRMAINT_API_TOKEN env var.")

        self._api_token = token.strip()
        self._rate_limiter = RateLimiter()
        self._http = httpx.Client(
            base_url=_BASE_URL,
            headers={"Authorization": f"Bearer {self._api_token}"},
            timeout=30.0,
        )

        self.assets = AssetsResource(self)
        self.locations = LocationsResource(self)
        self.production_areas = ProductionAreasResource(self)
        self.production_lines = ProductionLinesResource(self)
        self.downtimes = DowntimesResource(self)
        self.failure_codes = FailureCodesResource(self)
        self.parts = PartsResource(self)
        self.andon_calls = AndonCallsResource(self)
        self.inventory = InventoryResource(self)
        self.attachments = AttachmentsResource(self)
        self.dictionaries = DictionariesResource(self)
        self.purchase_requests = PurchaseRequestsResource(self)
        self.shifts = ShiftsResource(self)
        self.stocks = StocksResource(self)
        self.storage_places = StoragePlacesResource(self)
        self.tags = TagsResource(self)
        self.teams = TeamsResource(self)
        self.users = UsersResource(self)
        self.vendors = VendorsResource(self)
        self.work_orders = WorkOrdersResource(self)
        self.work_requests = WorkRequestsResource(self)

        self._initialized = True

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        """Acquire a rate-limit slot, issue the request, and return the payload.

        Args:
            method: HTTP verb (``"GET"``, ``"POST"``, etc.).
            path: API path relative to the base URL.
            **kwargs: Additional keyword arguments forwarded to ``httpx``.

        Returns:
            The unwrapped ``payload`` dict from the API response envelope.

        Raises:
            AuthenticationError: On HTTP 401.
            NotFoundError: On HTTP 404.
            RateLimitError: On HTTP 429.
            APIError: On any other 4xx or 5xx response.
        """
        self._rate_limiter.acquire()
        response = self._http.request(method, path, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict:
        """Parse an httpx response and raise the appropriate exception on error.

        The API wraps every successful response in an envelope of the form
        ``{"status": "SUCCESS", "payload": {...}, "error": null}``.  This
        method unwraps that envelope and returns only the ``payload`` value.

        Args:
            response: The raw ``httpx.Response`` object.

        Returns:
            The ``payload`` value from the response body, or the full body
            dict when the ``payload`` key is absent.

        Raises:
            AuthenticationError: On HTTP 401.
            NotFoundError: On HTTP 404.
            RateLimitError: On HTTP 429.
            APIError: On any other 4xx or 5xx response.
        """
        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired API token.")
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.url}")
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(float(retry_after) if retry_after else None)
        if response.status_code >= 400:
            try:
                body = response.json()
                msg = body.get("error") or body.get("message") or response.text
            except Exception:
                msg = response.text
            raise APIError(response.status_code, msg)
        body = response.json()
        return body.get("payload", body)

    def close(self) -> None:
        """Close the underlying HTTP connection pool.

        Call this when you are done with the client and are not using it as a
        context manager.
        """
        self._http.close()

    def __enter__(self) -> QrMaintClient:
        """Support usage as a context manager.

        Returns:
            The client instance itself.
        """
        return self

    def __exit__(self, *_: object) -> None:
        """Close the HTTP client when leaving the ``with`` block."""
        self.close()
