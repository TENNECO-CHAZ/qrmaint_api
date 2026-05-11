"""Resource class for the Purchase Requests endpoint (/purchase-requests)."""
from __future__ import annotations

from datetime import datetime

from ..models.common import PaginatedResponse, UpdatedObject
from ..models.purchase_requests import PurchaseRequest, UpdatedPurchaseRequestParams
from .base import BaseResource


class PurchaseRequestsResource(BaseResource):
    """Provides read and update operations for QrMaint purchase requests.

    Access via ``client.purchase_requests``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 100,
        created_datetime_from: datetime | None = None,
        created_datetime_to: datetime | None = None,
        modified_datetime_from: datetime | None = None,
        modified_datetime_to: datetime | None = None,
        last_id: int | None = None,
        type_id: int | None = None,
        status_id: int | None = None,
    ) -> PaginatedResponse[PurchaseRequest]:
        """Return a paginated list of purchase requests.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            created_datetime_from: Return requests created on or after this UTC
                timestamp.
            created_datetime_to: Return requests created before or on this UTC
                timestamp.
            modified_datetime_from: Return requests last modified on or after
                this UTC timestamp.
            modified_datetime_to: Return requests last modified before or on
                this UTC timestamp.
            last_id: Return requests with an ID greater than this value (cursor
                pagination).
            type_id: Filter to requests of this type.
            status_id: Filter to requests in this status.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.purchase_requests.PurchaseRequest` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "createdDatetimeFrom": created_datetime_from.isoformat() if created_datetime_from else None,
            "createdDatetimeTo": created_datetime_to.isoformat() if created_datetime_to else None,
            "modifiedDatetimeFrom": modified_datetime_from.isoformat() if modified_datetime_from else None,
            "modifiedDatetimeTo": modified_datetime_to.isoformat() if modified_datetime_to else None,
            "lastId": last_id,
            "typeId": type_id,
            "statusId": status_id,
        })
        return self._parse_paginated(self._get("/purchase-requests", params=params), PurchaseRequest)

    def get(self, request_id: int) -> PurchaseRequest:
        """Fetch a single purchase request including its line items.

        Args:
            request_id: Internal integer ID of the purchase request.

        Returns:
            The matching :class:`~qrmaint_api.models.purchase_requests.PurchaseRequest`
            with its ``items`` list populated.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no request matches the given ID.
        """
        return self._parse_single(self._get(f"/purchase-requests/{request_id}"), PurchaseRequest)

    def update(self, request_id: int, params: UpdatedPurchaseRequestParams) -> UpdatedObject:
        """Partially update an existing purchase request.

        Args:
            request_id: Internal integer ID of the purchase request.
            params: Fields to update; omitted fields are left unchanged.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no request matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._patch(f"/purchase-requests/{request_id}", json=body), UpdatedObject)
