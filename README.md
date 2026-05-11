# qrmaint-api

A typed Python client for the [QrMaint REST API](https://api.qrmaint.com/docs-v1/index.html).

- **Singleton** — one shared client instance per process
- **Rate-limited** — automatically respects all four official windows (10/s · 9 000/15 min · 45 000/12 h · 1 000 000/7 days)
- **Typed** — every response is a Pydantic v2 model, not a raw dict

## Requirements

- Python ≥ 3.11
- `httpx >= 0.27`
- `pydantic >= 2.7`
- `limits >= 3.9`

## Installation

```bash
pip install qrmaint-api
```

Or, for local development:

```bash
pip install -e ".[dev]"
```

## Quick start

```python
from qrmaint_api import QrMaintClient

client = QrMaintClient(api_token="your-token-here")

# List the first page of assets
response = client.assets.list(per_page=50)
print(f"{response.all_records_count} assets total")
for asset in response.data:
    print(asset.id, asset.name)
```

You can also set the token via the `QRMAINT_API_TOKEN` environment variable and call `QrMaintClient()` with no arguments.

## Pagination

All list endpoints return a `PaginatedResponse[T]` with two fields:

| Field | Type | Description |
|---|---|---|
| `data` | `list[T]` | Records on the current page |
| `all_records_count` | `int` | Total number of matching records |

Example — fetch every asset:

```python
assets = []
page = 1
while True:
    response = client.assets.list(page=page, per_page=100)
    assets.extend(response.data)
    if len(assets) >= response.all_records_count:
        break
    page += 1
```

## Available resources

| Attribute | Endpoint | Operations |
|---|---|---|
| `client.assets` | `/assets` | `list`, `get`, `create`, `update`, `get_planned_production_time` |
| `client.locations` | `/locations` | `list`, `get`, `create`, `update` |
| `client.production_areas` | `/production-areas` | `list`, `get`, `create`, `update` |
| `client.production_lines` | `/production-lines` | `list`, `get`, `create`, `update` |
| `client.work_orders` | `/work-orders` | `list`, `get`, `create`, `update`, `assign_assets`, `assign_users`, `assign_teams`, `assign_shifts` |
| `client.work_requests` | `/work-requests` | `list`, `get`, `create` |
| `client.downtimes` | `/downtimes` | `list`, `get`, `create` |
| `client.parts` | `/parts` | `list`, `create` |
| `client.stocks` | `/stocks` | `list`, `update`, `adjust_items`, `list_logs` |
| `client.inventory` | `/inventory-documents` | `list_documents`, `create_document`, `list_document_items`, `add_document_item`, `list_stock_logs`, `adjust_stock` |
| `client.purchase_requests` | `/purchase-requests` | `list`, `get`, `update` |
| `client.vendors` | `/vendors` | `list`, `get`, `create`, `update` |
| `client.storage_places` | `/dictionaries/storage-places` | `list`, `get`, `create`, `update` |
| `client.dictionaries` | `/dictionaries` | `list_root_parents`, `list_items`, `create_item`, `update_item` |
| `client.attachments` | `/attachments` | `list`, `get`, `get_download_url` |
| `client.tags` | `/tags` | `list` |
| `client.teams` | `/teams` | `list` |
| `client.users` | `/users` | `list` |
| `client.shifts` | `/shifts` | `list` |
| `client.andon_calls` | `/andon-calls` | `list`, `list_types` |

## Using external IDs

Several resources accept an `id_type` keyword argument to look up or update records by their caller-supplied external identifier instead of the internal integer ID:

```python
from qrmaint_api import IdType

asset = client.assets.get("EXT-001", id_type=IdType.EXTERNAL_ID)
```

## Error handling

All errors are subclasses of `QrMaintError`:

| Exception | When raised |
|---|---|
| `AuthenticationError` | Invalid or missing API token (HTTP 401) |
| `NotFoundError` | Resource not found (HTTP 404) |
| `RateLimitError` | Server-side rate limit hit (HTTP 429) |
| `APIError` | Any other non-2xx response |

```python
from qrmaint_api import QrMaintClient, NotFoundError

client = QrMaintClient()
try:
    asset = client.assets.get(99999)
except NotFoundError:
    print("Asset not found")
```

## Context manager & cleanup

```python
with QrMaintClient(api_token="...") as client:
    assets = client.assets.list()
# HTTP connection pool is closed automatically
```

## License

MIT
