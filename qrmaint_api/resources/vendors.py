"""Resource class for the Vendors endpoint (/vendors)."""

from ..models.common import CreatedObject, PaginatedResponse, UpdatedObject
from ..models.vendors import Vendor, VendorParams, UpdatedVendorParams
from .base import BaseResource


class VendorsResource(BaseResource):
    """Provides CRUD operations for QrMaint vendors (suppliers).

    Access via ``client.vendors``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
    ) -> PaginatedResponse[Vendor]:
        """Return a paginated list of vendors.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to vendor name.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.vendors.Vendor` objects.
        """
        params = self._clean_params({"page": page, "perPage": per_page, "query": query})
        return self._parse_paginated(self._get("/vendors", params=params), Vendor)

    def get(self, vendor_id: int) -> Vendor:
        """Fetch a single vendor by its internal ID.

        Args:
            vendor_id: Internal integer ID of the vendor.

        Returns:
            The matching :class:`~qrmaint_api.models.vendors.Vendor`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no vendor matches the given ID.
        """
        return self._parse_single(self._get(f"/vendors/{vendor_id}"), Vendor)

    def create(self, params: VendorParams) -> CreatedObject:
        """Create a new vendor.

        Args:
            params: Field values for the new vendor.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new vendor's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/vendors", json=body), CreatedObject)

    def update(self, vendor_id: int, params: UpdatedVendorParams) -> UpdatedObject:
        """Partially update an existing vendor.

        Args:
            vendor_id: Internal integer ID of the vendor.
            params: Fields to update; omitted fields are left unchanged.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no vendor matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._patch(f"/vendors/{vendor_id}", json=body), UpdatedObject)
