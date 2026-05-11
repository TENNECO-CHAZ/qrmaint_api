"""Resource class for the Work Orders endpoint (/work-orders)."""

from datetime import datetime

from ..models.common import CreatedObject, PaginatedResponse, UpdatedObject
from ..models.work_orders import (
    PriorityType,
    UpdatedWorkOrderParams,
    WorkGroup,
    WorkOrder,
    WorkOrderAssetsOrLocationsAssignmentParams,
    WorkOrderParams,
    WorkOrderShiftsAssignmentParams,
    WorkOrderTeamsAssignmentParams,
    WorkOrderUsersAssignmentParams,
)
from .base import BaseResource


class WorkOrdersResource(BaseResource):
    """Provides CRUD and assignment operations for QrMaint work orders.

    Access via ``client.work_orders``.
    """

    def list(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
        query: str | None = None,
        status_ids: list[int] | None = None,
        priority_ids: list[PriorityType] | None = None,
        type_of_work_ids: list[int] | None = None,
        created_datetime_from: datetime | None = None,
        created_datetime_to: datetime | None = None,
        completed_datetime_from: datetime | None = None,
        completed_datetime_to: datetime | None = None,
        modified_datetime_from: datetime | None = None,
        modified_datetime_to: datetime | None = None,
        asset_or_location_id: int | None = None,
        last_id: int | None = None,
        work_group: WorkGroup | None = None,
    ) -> PaginatedResponse[WorkOrder]:
        """Return a paginated list of work orders.

        Args:
            page: 1-based page number.
            per_page: Number of records per page (max 100).
            query: Free-text search applied to work order title and number.
            status_ids: Filter to work orders in any of these statuses.
            priority_ids: Filter to work orders with any of these priorities.
            type_of_work_ids: Filter to work orders of these work types.
            created_datetime_from: Return orders created on or after this UTC
                timestamp.
            created_datetime_to: Return orders created before or on this UTC
                timestamp.
            completed_datetime_from: Return orders completed on or after this
                UTC timestamp.
            completed_datetime_to: Return orders completed before or on this
                UTC timestamp.
            modified_datetime_from: Return orders last modified on or after
                this UTC timestamp.
            modified_datetime_to: Return orders last modified before or on
                this UTC timestamp.
            asset_or_location_id: Filter to orders linked to this asset or
                location.
            last_id: Return orders with an ID greater than this value (cursor
                pagination).
            work_group: Scope filter — ``MY``, ``ALL``, or ``UNASSIGNED``.

        Returns:
            A :class:`~qrmaint_api.models.common.PaginatedResponse` containing
            :class:`~qrmaint_api.models.work_orders.WorkOrder` objects.
        """
        params = self._clean_params({
            "page": page,
            "perPage": per_page,
            "query": query,
            "statusIds": status_ids,
            "priorityIds": [p.value for p in priority_ids] if priority_ids else None,
            "typeOfWorkIds": type_of_work_ids,
            "createdDatetimeFrom": created_datetime_from.isoformat() if created_datetime_from else None,
            "createdDatetimeTo": created_datetime_to.isoformat() if created_datetime_to else None,
            "completedDatetimeFrom": completed_datetime_from.isoformat() if completed_datetime_from else None,
            "completedDatetimeTo": completed_datetime_to.isoformat() if completed_datetime_to else None,
            "modifiedDatetimeFrom": modified_datetime_from.isoformat() if modified_datetime_from else None,
            "modifiedDatetimeTo": modified_datetime_to.isoformat() if modified_datetime_to else None,
            "assetOrLocationId": asset_or_location_id,
            "lastId": last_id,
            "workGroup": work_group.value if work_group else None,
        })
        return self._parse_paginated(self._get("/work-orders", params=params), WorkOrder)

    def get(self, work_order_id: int) -> WorkOrder:
        """Fetch a single work order by its internal ID.

        Args:
            work_order_id: Internal integer ID of the work order.

        Returns:
            The matching :class:`~qrmaint_api.models.work_orders.WorkOrder`.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no work order matches the given ID.
        """
        return self._parse_single(self._get(f"/work-orders/{work_order_id}"), WorkOrder)

    def create(self, params: WorkOrderParams) -> CreatedObject:
        """Create a new work order.

        Args:
            params: Field values for the new work order.

        Returns:
            A :class:`~qrmaint_api.models.common.CreatedObject` containing the
            new work order's ``id``.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._post("/work-orders", json=body), CreatedObject)

    def update(self, work_order_id: int, params: UpdatedWorkOrderParams) -> UpdatedObject:
        """Partially update an existing work order.

        Args:
            work_order_id: Internal integer ID of the work order.
            params: Fields to update; omitted fields are left unchanged.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            update.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no work order matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._patch(f"/work-orders/{work_order_id}", json=body), UpdatedObject)

    def assign_assets(self, work_order_id: int, params: WorkOrderAssetsOrLocationsAssignmentParams) -> UpdatedObject:
        """Replace the asset and location assignments on a work order.

        Args:
            work_order_id: Internal integer ID of the work order.
            params: New set of asset IDs, asset external IDs, and/or location
                IDs.  This call replaces any existing assignments.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            assignment.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no work order matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put(f"/work-orders/{work_order_id}/assets", json=body), UpdatedObject)

    def assign_users(self, work_order_id: int, params: WorkOrderUsersAssignmentParams) -> UpdatedObject:
        """Replace the user assignments on a work order.

        Args:
            work_order_id: Internal integer ID of the work order.
            params: New set of user IDs.  This call replaces any existing
                user assignments.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            assignment.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no work order matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put(f"/work-orders/{work_order_id}/users", json=body), UpdatedObject)

    def assign_teams(self, work_order_id: int, params: WorkOrderTeamsAssignmentParams) -> UpdatedObject:
        """Replace the team assignments on a work order.

        Args:
            work_order_id: Internal integer ID of the work order.
            params: New set of team IDs.  This call replaces any existing
                team assignments.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            assignment.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no work order matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put(f"/work-orders/{work_order_id}/teams", json=body), UpdatedObject)

    def assign_shifts(self, work_order_id: int, params: WorkOrderShiftsAssignmentParams) -> UpdatedObject:
        """Replace the shift assignments on a work order.

        Args:
            work_order_id: Internal integer ID of the work order.
            params: New set of shift IDs.  This call replaces any existing
                shift assignments.

        Returns:
            An :class:`~qrmaint_api.models.common.UpdatedObject` confirming the
            assignment.

        Raises:
            ~qrmaint_api.exceptions.NotFoundError: If no work order matches the given ID.
        """
        body = params.model_dump(by_alias=True, exclude_none=True)
        return self._parse_single(self._put(f"/work-orders/{work_order_id}/shifts", json=body), UpdatedObject)
