"""Resource class for the Dictionaries endpoint (/dictionaries)."""
from __future__ import annotations

from ..models.common import CreatedObject, DictionaryItemType, PaginatedResponse, UpdatedObject
from ..models.dictionaries import (
    DictionariesItem,
    DictionariesItemParams,
    DictionaryItem,
    DictionaryRootParent,
    UpdatedDictionaryItemParams,
)
from .base import BaseResource


class DictionariesResource(BaseResource):
    """Provides CRUD operations for QrMaint configurable dictionaries.

    Dictionaries are key-value stores that back dropdowns such as failure codes,
    work types, and priorities.

    Access via ``client.dictionaries``.
    """

    def list_root_parents(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> PaginatedResponse[DictionaryRootParent]:
        """Return a paginated list of top-level dictionary categories.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.dictionaries.DictionaryRootParent` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page})
        return self._parse_paginated(self._get("/dictionaries", params=params), DictionaryRootParent)

    def list_items(
        self,
        root_parent_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[DictionariesItem]:
        """Return a paginated list of items within a dictionary category.

        Args:
            root_parent_id: Internal ID of the top-level dictionary.
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to item name.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.dictionaries.DictionariesItem` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        path = f"/dictionaries/{root_parent_id}/items"
        return self._parse_paginated(self._get(path, params=params), DictionariesItem)

    def create_item(self, root_parent_id: int, params: DictionariesItemParams) -> CreatedObject:
        """Add a new item to a dictionary category.

        Args:
            root_parent_id: Internal ID of the target top-level dictionary.
            params: Field values for the new item.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new item's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post(f"/dictionaries/{root_parent_id}/items", json=body), CreatedObject)

    def list_by_type(
        self,
        parent_type: DictionaryItemType,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[DictionaryItem]:
        """Return dictionary items filtered by a built-in parent type.

        Uses the legacy ``/dictionary-items`` endpoint (⚠️ limited support).

        Args:
            parent_type: Category to filter by (see
                :class:`~qrmaint_api.models.common.DictionaryItemType`).
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to item name.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.dictionaries.DictionaryItem` objects.
        """
        params = self._clean_params({
            "parentType": parent_type.value,
            "page": page,
            "perPage": per_page,
            "query": query,
        })
        return self._parse_paginated(self._get("/dictionary-items", params=params), DictionaryItem)

    def update_item(
        self,
        root_parent_id: int,
        item_id: int,
        params: UpdatedDictionaryItemParams,
    ) -> UpdatedObject:
        """Partially update a dictionary item.

        Args:
            root_parent_id: Internal ID of the owning dictionary.
            item_id: Internal integer ID of the item to update.
            params: Fields to update; omitted fields are left unchanged.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no item matches the given IDs.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        path = f"/dictionaries/{root_parent_id}/items/{item_id}"
        return self._parse_single(self._patch(path, json=body), UpdatedObject)
