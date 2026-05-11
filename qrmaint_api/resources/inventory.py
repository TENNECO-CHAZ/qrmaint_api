"""Resource class for the Inventory endpoints (/inventory-documents, /inventory-stock-logs)."""

from ..models.common import CreatedObject, PaginatedResponse
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
    ) -> PaginatedResponse[InventoryDocument]:
        """Return a paginated list of inventory documents.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to document number and description.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.inventory.InventoryDocument` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
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
        part_id: int | None = None,
    ) -> PaginatedResponse[InventoryStockLog]:
        """Return a paginated list of inventory stock movement logs.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            part_id: Filter to movements for this part.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.inventory.InventoryStockLog` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "partId": part_id})
        return self._parse_paginated(self._get("/inventory-stock-logs", params=params), InventoryStockLog)

    def adjust_stock(self, params: InventoryStockAdjustingParams) -> CreatedObject:
        """Create a stock adjustment via the inventory-stock-adjustments endpoint.

        This creates a CORRECTION-type inventory document and updates stock
        levels atomically.

        Args:
            params: Adjustment details including warehouse, part, quantity, and
                pricing information.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new adjustment document's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/inventory-stock-adjustments", json=body), CreatedObject)
