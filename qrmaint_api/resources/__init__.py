"""Public resource exports for the ``qrmaint_api.resources`` package.

Each resource class wraps one API domain and is exposed as an attribute on
:class:`~qrmaint_api.client.QrMaintClient`::

    client.assets        # AssetsResource
    client.work_orders   # WorkOrdersResource
    # … etc.
"""
from __future__ import annotations

from .andon_calls import AndonCallsResource
from .assets import AssetsResource
from .attachments import AttachmentsResource
from .dictionaries import DictionariesResource
from .downtimes import DowntimesResource
from .inventory import InventoryResource
from .locations import LocationsResource
from .parts import PartsResource
from .production_areas import ProductionAreasResource
from .production_lines import ProductionLinesResource
from .purchase_requests import PurchaseRequestsResource
from .shifts import ShiftsResource
from .stocks import StocksResource
from .storage_places import StoragePlacesResource
from .tags import TagsResource
from .teams import TeamsResource
from .users import UsersResource
from .vendors import VendorsResource
from .work_orders import WorkOrdersResource
from .work_requests import WorkRequestsResource

__all__ = [
    "AndonCallsResource",
    "AssetsResource",
    "AttachmentsResource",
    "DictionariesResource",
    "DowntimesResource",
    "InventoryResource",
    "LocationsResource",
    "PartsResource",
    "ProductionAreasResource",
    "ProductionLinesResource",
    "PurchaseRequestsResource",
    "ShiftsResource",
    "StocksResource",
    "StoragePlacesResource",
    "TagsResource",
    "TeamsResource",
    "UsersResource",
    "VendorsResource",
    "WorkOrdersResource",
    "WorkRequestsResource",
]
