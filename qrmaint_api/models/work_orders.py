"""Pydantic models for the Work Orders domain."""

from datetime import datetime
from enum import Enum

from .common import _CamelModel


class PriorityType(str, Enum):
    """Priority level for a work order."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class WorkGroup(str, Enum):
    """Filter scope for listing work orders."""

    MY = "MY"
    ALL = "ALL"
    UNASSIGNED = "UNASSIGNED"


class AssignedResource(_CamelModel):
    """An asset or location assigned to a work order."""

    id: int
    name: str | None = None
    number: str | None = None
    external_id: str | None = None
    type_id: int | None = None
    type_name: str | None = None
    resource_type: str | None = None


class AssignedUser(_CamelModel):
    id: int
    name: str | None = None


class AssignedTeam(_CamelModel):
    id: int
    name: str | None = None


class AssignedShift(_CamelModel):
    id: int
    name: str | None = None


class AssignedTag(_CamelModel):
    id: int
    name: str | None = None


class WorkOrderAttachment(_CamelModel):
    id: int
    file_name: str | None = None
    size: int | None = None
    type: str | None = None
    type_group: str | None = None
    created_datetime: datetime | None = None


class WorkOrder(_CamelModel):
    """A maintenance work order returned by the QrMaint API."""

    id: int
    client_id: int | None = None
    number: str | None = None
    subject: str | None = None
    description: str | None = None
    created_datetime: datetime | None = None
    modified_datetime: datetime | None = None
    created_user_id: int | None = None
    created_user_name: str | None = None
    created_user_email: str | None = None
    created_user_phone_number: str | None = None
    completed_datetime: datetime | None = None
    completed_user_id: int | None = None
    completed_user_name: str | None = None
    technical_remarks: str | None = None
    non_public: bool | None = None
    priority: PriorityType | None = None
    problem_id: int | None = None
    problem_name: str | None = None
    failure_code_id: int | None = None
    failure_code_name: str | None = None
    status_id: int | None = None
    status_name: str | None = None
    type_of_work_id: int | None = None
    type_of_work_name: str | None = None
    customer_id: int | None = None
    customer_name: str | None = None
    vendor_id: int | None = None
    vendor_name: str | None = None
    is_vendor_confirm_email_send: bool | None = None
    vendor_request_sent_datetime: datetime | None = None
    vendor_confirm_datetime: datetime | None = None
    vendor_completed_datetime: datetime | None = None
    all_day: bool | None = None
    due_date_from: datetime | None = None
    due_date_to: datetime | None = None
    total_duration_seconds: int | None = None
    downtime_id: int | None = None
    downtime_duration_seconds: int | None = None
    downtime_start_datetime: datetime | None = None
    is_downtime_end: bool | None = None
    asset_release_to_work_user_id: int | None = None
    asset_release_to_work_user_name: str | None = None
    asset_release_to_work_date_time: datetime | None = None
    is_clean_required: bool | None = None
    clean_request_confirm_datetime: datetime | None = None
    clean_request_confirm_user_id: int | None = None
    clean_request_confirm_user_name: str | None = None
    clean_confirm_datetime: datetime | None = None
    clean_confirm_user_id: int | None = None
    clean_confirm_user_name: str | None = None
    checklist_warning: bool | None = None
    is_preventive_work: bool | None = None
    influence_on_production_cycle_time: bool | None = None
    estimated_total_time_seconds: int | None = None
    asset_shutdown_required: bool | None = None
    assigned_assets_or_locations: list[AssignedResource] = []
    assigned_users: list[AssignedUser] = []
    assigned_teams: list[AssignedTeam] = []
    assigned_shifts: list[AssignedShift] = []
    tags: list[AssignedTag] = []
    attachments: list[WorkOrderAttachment] = []


class WorkOrderParams(_CamelModel):
    """Request body for creating a new work order (POST /work-orders)."""

    subject: str
    priority: PriorityType | None = None
    due_date_from: datetime | None = None
    due_date_to: datetime | None = None
    description: str | None = None
    type_of_work_id: int | None = None
    failure_code_id: int | None = None
    estimated_total_time_seconds: int | None = None


class UpdatedWorkOrderParams(_CamelModel):
    """Request body for partially updating a work order (PATCH /work-orders/{id})."""

    subject: str | None = None
    status_id: int | None = None
    priority: PriorityType | None = None
    type_of_work_id: int | None = None
    failure_code_id: int | None = None
    description: str | None = None
    due_date_from: datetime | None = None
    due_date_to: datetime | None = None
    estimated_total_time_seconds: int | None = None
    completed_datetime: datetime | None = None


class WorkOrderAssetsOrLocationsAssignmentParams(_CamelModel):
    """Request body for assigning assets or locations to a work order."""

    asset_ids: list[int] | None = None
    asset_external_ids: list[str] | None = None
    location_ids: list[int] | None = None


class WorkOrderUsersAssignmentParams(_CamelModel):
    """Request body for assigning users to a work order."""

    user_ids: list[int]


class WorkOrderTeamsAssignmentParams(_CamelModel):
    """Request body for assigning teams to a work order."""

    team_ids: list[int]


class WorkOrderShiftsAssignmentParams(_CamelModel):
    """Request body for assigning shifts to a work order."""

    shift_ids: list[int]
