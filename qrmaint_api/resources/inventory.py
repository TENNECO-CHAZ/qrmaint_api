"""Resource class for the Inventory endpoints (/inventory-documents, /inventory-stock-logs)."""
from __future__ import annotations

from datetime import datetime

from ..models.common import CreatedObject, PaginatedResponse, UpdatedObject
from ..models.inventory import (
    InventoryDocument,
    InventoryDocumentItem,
    InventoryDocumentParams,
    InventoryStockAdjustingParams,
    InventoryStockLog,
    NewInventoryDocumentItemParams,
)
from .base import BaseResource


class InventoryResource(BaseResource):
    """Provides operations for QrMaint inventory documents and stock adjustments.

    Access via ``client.inventory``.
    """

    def list_documents(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
        created_datetime_from: datetime | None = None,
        created_datetime_to: datetime | None = None,
    ) -> PaginatedResponse[InventoryDocument]:
        """Return a paginated list of inventory documents.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to document number and name.
            created_datetime_from: Return documents created on or after this UTC timestamp.
            created_datetime_to: Return documents created before or on this UTC timestamp.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.inventory.InventoryDocument` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "createdDatetimeFrom": created_datetime_from.isoformat() if created_datetime_from else None,
            "createdDatetimeTo": created_datetime_to.isoformat() if created_datetime_to else None,
        })
        return self._parse_paginated(self._get("/inventory-documents", params=params), InventoryDocument)

    def create_document(self, params: InventoryDocumentParams) -> CreatedObject:
        """Create a new inventory document.

        Args:
            params: Field values for the new document.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new document's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/inventory-documents", json=body), CreatedObject)

    def get_document(self, document_id: int) -> InventoryDocument:
        """Fetch a single inventory document by its internal ID.

        Args:
            document_id: Internal integer ID of the inventory document.

        Returns:
            The matching :class:`~qrmaint_api.models.inventory.InventoryDocument`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no document matches the given ID.
        """
        return self._parse_single(self._get(f"/inventory-documents/{document_id}"), InventoryDocument)

    def list_document_items(
        self,
        document_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> PaginatedResponse[InventoryDocumentItem]:
        """Return the line items of an inventory document.

        Args:
            document_id: Internal integer ID of the parent document.
            page: 1-based page number.
            per_page: Number of records per page (max 100).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.inventory.InventoryDocumentItem` objects.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no document matches the given ID.
        """
        params = self._clean_params({"page": page, "perPage": per_page})
        path = f"/inventory-documents/{document_id}/items"
        return self._parse_paginated(self._get(path, params=params), InventoryDocumentItem)

    def get_document_item(self, document_id: int, item_id: int) -> InventoryDocumentItem:
        """Fetch a single inventory document line item.

        Args:
            document_id: Internal integer ID of the parent inventory document.
            item_id: Internal integer ID of the line item.

        Returns:
            The matching :class:`~qrmaint_api.models.inventory.InventoryDocumentItem`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no document or item matches.
        """
        path = f"/inventory-documents/{document_id}/items/{item_id}"
        return self._parse_single(self._get(path), InventoryDocumentItem)

    def add_document_item(self, document_id: int, params: NewInventoryDocumentItemParams) -> CreatedObject:
        """Add a line item to an existing inventory document.

        Args:
            document_id: Internal integer ID of the parent document.
            params: Field values for the new line item.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new item's ``id``.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no document matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post(f"/inventory-documents/{document_id}/items", json=body), CreatedObject)

    def list_stock_logs(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        datetime_from: datetime | None = None,
        datetime_to: datetime | None = None,
        part_id: int | None = None,
        part_external_id: str | None = None,
        inventory_id: int | None = None,
        last_id: int | None = None,
    ) -> PaginatedResponse[InventoryStockLog]:
        """Return a paginated list of inventory stock movement logs (deprecated).

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            datetime_from: Return entries created on or after this timestamp.
            datetime_to: Return entries created before or on this timestamp.
            part_id: Filter to movements for this part.
            part_external_id: Filter by the part's external identifier.
            inventory_id: Filter by inventory ID.
            last_id: Return entries with an ID greater than this value (cursor pagination).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.inventory.InventoryStockLog` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "datetimeFrom": datetime_from.isoformat() if datetime_from else None,
            "datetimeTo": datetime_to.isoformat() if datetime_to else None,
            "partId": part_id,
            "partExternalId": part_external_id,
            "inventoryId": inventory_id,
            "lastId": last_id,
        })
        return self._parse_paginated(self._get("/inventory-stock-logs", params=params), InventoryStockLog)

    def adjust_stock(self, params: InventoryStockAdjustingParams) -> UpdatedObject:
        """Bulk-adjust inventory stock via the legacy inventory-stocks endpoint.

        Args:
            params: List of stock items with inventory ID, part, quantity, and pricing.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            adjustment.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put("/inventory-stocks/adjust-items", json=body), UpdatedObject)
