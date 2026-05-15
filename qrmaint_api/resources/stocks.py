"""Resource class for the Stocks endpoints (/stocks, /stocks-logs)."""
from __future__ import annotations

from datetime import datetime

from ..exceptions import APIError, StockSyncValidationError
from ..models.common import PaginatedResponse, UpdatedObject
from ..models.stocks import (
    Stock,
    StockAdjustingParams,
    StockLog,
    SyncStockQuantitiesParams,
    SyncStockQuantityInvalidItem,
    UpdatedStockParams,
)
from .base import BaseResource


class StocksResource(BaseResource):
    """Provides operations for QrMaint stock levels and movement logs.

    Access via ``client.stocks``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        part_id: int | None = None,
        part_external_id: str | None = None,
        warehouse_id: int | None = None,
    ) -> PaginatedResponse[Stock]:
        """Return a paginated list of stock records.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            part_id: Filter to stock records for this part.
            part_external_id: Filter by the part's external identifier.
            warehouse_id: Filter to stock held in this warehouse.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.stocks.Stock` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "partId": part_id,
            "partExternalId": part_external_id,
            "warehouseId": warehouse_id,
        })
        return self._parse_paginated(self._get("/stocks", params=params), Stock)

    def update(self, stock_id: int, params: UpdatedStockParams) -> UpdatedObject:
        """Partially update a stock record's thresholds or storage location.

        Args:
            stock_id: Internal integer ID of the stock record.
            params: Fields to update; omitted fields are left unchanged.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no stock record matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._patch(f"/stocks/{stock_id}", json=body), UpdatedObject)

    def adjust_items(self, params: StockAdjustingParams) -> UpdatedObject:
        """Bulk-adjust stock quantities via the legacy adjust-items endpoint.

        .. deprecated::
            Prefer :meth:`~qrmaint_api.resources.inventory.InventoryResource.adjust_stock`
            which creates a proper CORRECTION inventory document.

        Args:
            params: List of stock items with their new quantities and pricing.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            adjustment.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put("/stocks/adjust-items", json=body), UpdatedObject)

    def sync_quantities(self, params: SyncStockQuantitiesParams) -> None:
        """Overwrite stock quantities and unit prices for multiple items in one transaction.

        All rows are processed atomically: if any item fails validation the
        entire batch is rolled back and a
        :class:`~qrmaint_api.exceptions.StockSyncValidationError` is raised with
        the list of rejected rows.

        Args:
            params: Up to 100 stock lines, each identifying the part and
                warehouse (by internal ID or external ID) plus the target
                quantity and unit price.

        Raises:
            ~qrmaint_api.exceptions.StockSyncValidationError: If any item fails
                validation (HTTP 400).  ``exc.invalid_items`` is a list of
                :class:`~qrmaint_api.models.stocks.SyncStockQuantityInvalidItem`
                describing each rejected row.
            ~qrmaint_api.exceptions.NotFoundError: If a referenced part or
                warehouse does not exist or does not belong to the client.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        try:
            self._put("/stocks/sync-quantities", json=body)
        except APIError as exc:
            if exc.status_code == 400 and isinstance(exc.payload, dict):
                raw_invalid = exc.payload.get("invalidItems") or []
                invalid_items = [SyncStockQuantityInvalidItem.model_validate(i) for i in raw_invalid]
                raise StockSyncValidationError(invalid_items) from exc
            raise

    def list_logs(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        created_datetime_from: datetime | None = None,
        created_datetime_to: datetime | None = None,
        part_id: int | None = None,
        part_external_id: str | None = None,
        warehouse_id: int | None = None,
        stock_movement_type_ids: list[int] | None = None,
        inventory_document_type_ids: list[int] | None = None,
        last_id: int | None = None,
        exclude_api_moves: bool | None = None,
    ) -> PaginatedResponse[StockLog]:
        """Return a paginated list of stock movement log entries.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            created_datetime_from: Return entries created on or after this UTC
                timestamp.
            created_datetime_to: Return entries created before or on this UTC
                timestamp.
            part_id: Filter to movements for this part.
            part_external_id: Filter by the part's external identifier.
            warehouse_id: Filter to movements in this warehouse.
            stock_movement_type_ids: Filter to specific movement type IDs.
            inventory_document_type_ids: Filter to movements triggered by
                documents of these types.
            last_id: Return entries with an ID greater than this value (cursor
                pagination).
            exclude_api_moves: When ``True``, exclude movements created by API
                (createdUserId = 100).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.stocks.StockLog` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "createdDatetimeFrom": created_datetime_from.isoformat() if created_datetime_from else None,
            "createdDatetimeTo": created_datetime_to.isoformat() if created_datetime_to else None,
            "partId": part_id,
            "partExternalId": part_external_id,
            "warehouseId": warehouse_id,
            "stockMovementTypeIds": stock_movement_type_ids,
            "inventoryDocumentTypeIds": inventory_document_type_ids,
            "lastId": last_id,
            "excludeApiMoves": exclude_api_moves,
        })
        return self._parse_paginated(self._get("/stocks-logs", params=params), StockLog)
