# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (`YYYY.MM.N`).

## [2026.5.2] - 2026-05-07

### Changed

- `Asset` model rewritten to match the actual API response: added `number`,
  `additional_info`, `parent_id`, `parent_external_id`, `parent_name`, `url`,
  `created_datetime`, `modified_datetime`, `created_user_id`, `modified_user_id`,
  `manufacturer_id`, `manufacturer_name`, `internal_number`, `type_id`, `type_name`,
  `is_public_request`, `criticality_id`, `criticality_name`, `cost_account_id`,
  `cost_account_name`, `vendor_id`, `vendor_name`, `status_id`, `status_name`,
  `production_date`, `installation_date`, `warranty_date`, `init_price`,
  full address block, `tags`, and `attachments`; removed stale fields
  (`location_id`, `location_name`, `status`, `category`, `manufacturer`,
  `qr_code`, `created_at`, `updated_at`).
- `AssetParams` / `UpdatedAssetParams` updated to use ID-based fields
  (`manufacturer_id`, `type_id`, `status_id`, `criticality_id`, `vendor_id`)
  and added date/price fields; removed `category` and plain `manufacturer`.
- `Location` model rewritten: added `number`, `additional_info`, `client_id`,
  `parent_external_id`, `located_at_id`, `created_datetime`, `modified_datetime`,
  `created_user_id`, `modified_user_id`, `type_id`, `type_name`, `cost_account_id`,
  `cost_account_name`, `is_public_request`, `is_parent_address`, full address block,
  and `attachments`; removed `description`, `parent_name`, `path`,
  `created_at`, `updated_at`.
- `LocationParams` / `UpdatedLocationParams` updated: replaced `description` with
  `additional_info`, added `located_at_id`, `type_id`, `cost_account_id`.
- `ProductionArea` model rewritten: added `number`, `additional_info`, `client_id`,
  `parent_external_id`, `located_at_id`, `created_datetime`, `modified_datetime`,
  `created_user_id`, `modified_user_id`, `is_public_request`, `is_parent_address`,
  `cost_account_id`, `cost_account_name`, full address block, `tags`, and
  `attachments`; removed `description`, `parent_name`, `type_id`, `type_name`,
  `created_at`, `updated_at`.
- `ProductionAreaParams` / `UpdatedProductionAreaParams` updated: replaced
  `description` with `additional_info`, added `located_at_id`, `cost_account_id`.
- `ProductionLine` model rewritten: added `number`, `additional_info`, `client_id`,
  `parent_external_id`, `url`, `created_datetime`, `modified_datetime`,
  `created_user_id`, `modified_user_id`, `is_public_request`, `cost_account_id`,
  `cost_account_name`, `status_id`, `status_name`, `tags`, and `attachments`;
  removed `location_id`, `location_name`, `created_at`, `updated_at`.
- `ProductionLineParams` / `UpdatedProductionLineParams` updated: added
  `additional_info`, `cost_account_id`, `status_id`.
- `AssetsResource.list()` now exposes `parent_id`, `parent_external_id`,
  `location_external_id`, and `tag_ids` filter parameters.
- `LocationsResource.list()` now exposes `parent_external_id` and `type_id`
  filter parameters.

### Added

- `EmbeddedTag` and `EmbeddedAttachment` shared models in `common.py` for
  inline tag/attachment objects returned inside resource responses.

## [2026.5.1] - 2026-05-06

### Added

- Singleton `QrMaintClient` with thread-safe instantiation.
- Automatic rate limiting across all four official QrMaint windows
  (10/s · 9 000/15 min · 45 000/12 h · 1 000 000/7 days).
- Pydantic v2 typed models for all 20 API domains.
- Resource classes: `assets`, `locations`, `production_areas`, `production_lines`,
  `work_orders`, `work_requests`, `downtimes`, `parts`, `stocks`, `inventory`,
  `purchase_requests`, `vendors`, `storage_places`, `dictionaries`, `attachments`,
  `tags`, `teams`, `users`, `shifts`, `andon_calls`.
- `IdType` support for fetching and updating records by external ID.
- Typed exception hierarchy: `AuthenticationError`, `NotFoundError`,
  `RateLimitError`, `APIError`.
- Context-manager support for clean connection-pool teardown.
- PEP 561 `py.typed` marker for downstream type checking.
