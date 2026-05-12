"""Public model exports for the ``qrmaint_api.models`` package.

Import any Pydantic model directly from this package rather than from the
individual submodules::

    from qrmaint_api.models import Asset, WorkOrder, PaginatedResponse
"""
from __future__ import annotations

from .common import (
    CreatedObject,
    DictionaryItemType,
    IdType,
    PaginatedResponse,
    UpdatedObject,
)
from .andon_calls import AndonCall
from .assets import Asset, AssetParams, AssetPlannedProductionTime, UpdatedAssetParams
from .attachments import Attachment, AttachmentDownloadUrl
from .dictionaries import DictionariesItem, DictionariesItemParams, DictionaryItem, DictionaryRootParent, UpdatedDictionaryItemParams
from .downtimes import Downtime, DowntimeParams
from .failure_codes import FailureCode
from .inventory import (
    InventoryDocument,
    InventoryDocumentItem,
    InventoryDocumentParams,
    InventoryStockAdjustingParams,
    InventoryStockLog,
    NewInventoryDocumentItemParams,
)
from .locations import Location, LocationParams, UpdatedLocationParams
from .parts import Part, PartParams, PartSupplier, PartSupplierParams, PartSupplierUpdateParams, PartUpdateParams
from .production_areas import ProductionArea, ProductionAreaParams, UpdatedProductionAreaParams
from .production_lines import ProductionLine, ProductionLineParams, UpdatedProductionLineParams
from .purchase_requests import PurchaseRequest, PurchaseRequestItem, UpdatedPurchaseRequestParams
from .shifts import Shift
from .stocks import Stock, StockAdjustingParams, StockItem, StockLog, UpdatedStockParams
from .storage_places import StoragePlace, StoragePlaceParams, UpdatedStoragePlaceParams
from .tags import Tag, TagType
from .teams import Team
from .users import User
from .vendors import UpdatedVendorParams, Vendor, VendorParams
from .work_orders import (
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
from .work_requests import WorkRequest, WorkRequestParams

__all__ = [
    "AndonCall",
    "Asset",
    "AssetParams",
    "AssetPlannedProductionTime",
    "Attachment",
    "AttachmentDownloadUrl",
    "CreatedObject",
    "DictionariesItem",
    "DictionariesItemParams",
    "DictionaryItem",
    "DictionaryItemType",
    "DictionaryRootParent",
    "Downtime",
    "DowntimeParams",
    "FailureCode",
    "IdType",
    "InventoryDocument",
    "InventoryDocumentItem",
    "InventoryDocumentParams",
    "InventoryStockAdjustingParams",
    "InventoryStockLog",
    "Location",
    "LocationParams",
    "NewInventoryDocumentItemParams",
    "PaginatedResponse",
    "Part",
    "PartParams",
    "PartSupplier",
    "PartSupplierParams",
    "PartSupplierUpdateParams",
    "PartUpdateParams",
    "PriorityType",
    "ProductionArea",
    "ProductionAreaParams",
    "ProductionLine",
    "ProductionLineParams",
    "PurchaseRequest",
    "PurchaseRequestItem",
    "Shift",
    "Stock",
    "StockAdjustingParams",
    "StockItem",
    "StockLog",
    "StoragePlace",
    "StoragePlaceParams",
    "Tag",
    "TagType",
    "Team",
    "UpdatedAssetParams",
    "UpdatedDictionaryItemParams",
    "UpdatedLocationParams",
    "UpdatedObject",
    "UpdatedProductionAreaParams",
    "UpdatedProductionLineParams",
    "UpdatedPurchaseRequestParams",
    "UpdatedStockParams",
    "UpdatedStoragePlaceParams",
    "UpdatedVendorParams",
    "UpdatedWorkOrderParams",
    "User",
    "Vendor",
    "VendorParams",
    "WorkGroup",
    "WorkOrder",
    "WorkOrderAssetsOrLocationsAssignmentParams",
    "WorkOrderParams",
    "WorkOrderShiftsAssignmentParams",
    "WorkOrderTeamsAssignmentParams",
    "WorkOrderUsersAssignmentParams",
    "WorkRequest",
    "WorkRequestParams",
]
