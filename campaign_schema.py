from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class SchemaField:
    name: str
    label: str
    dtype: str
    required: bool
    nullable: bool = True
    default: Any = None
    recommended_header: str | None = None
    aliases: tuple[str, ...] = field(default_factory=tuple)
    description: str = ""


CAMPAIGN_PLAN_SCHEMA: tuple[SchemaField, ...] = (
    SchemaField(
        "campaign_id",
        "Campaign code / ID",
        "string",
        True,
        nullable=False,
        recommended_header="campaign_code",
        aliases=(
            "campaign",
            "campaign id",
            "campaign_id",
            "campaign code",
            "campaign_code",
            "promo code",
            "promo_code",
            "promotion code",
            "promotion_code",
        ),
        description="Campaign, promo or pricing code used to identify the campaign.",
    ),
    SchemaField(
        "campaign_name",
        "Campaign name",
        "string",
        True,
        nullable=False,
        recommended_header="campaign_name",
        aliases=("campaign name", "campaign_name"),
        description="Human-readable campaign name.",
    ),
    SchemaField(
        "campaign_source",
        "Campaign source",
        "string",
        False,
        default="Uploaded file",
        recommended_header="campaign_source",
        aliases=("source", "campaign source", "campaign_source"),
        description="Where the plan came from.",
    ),
    SchemaField(
        "planned_start",
        "Campaign start date",
        "date",
        True,
        nullable=False,
        recommended_header="start_date",
        aliases=("start", "start date", "start_date", "campaign start date", "planned start", "planned_start"),
        description="Campaign launch date.",
    ),
    SchemaField(
        "planned_end",
        "Campaign end date",
        "date",
        True,
        nullable=False,
        recommended_header="end_date",
        aliases=("end", "end date", "end_date", "campaign end date", "planned end", "planned_end"),
        description="Campaign end date.",
    ),
    SchemaField(
        "channel",
        "Channel",
        "channel",
        True,
        nullable=False,
        recommended_header="channel",
        aliases=("channel",),
        description="Target selling channel.",
    ),
    SchemaField(
        "item_id",
        "Product SKU",
        "string",
        True,
        nullable=True,
        recommended_header="product_sku",
        aliases=("sku", "product sku", "product_sku", "item", "item id", "item_id", "product"),
        description="Product SKU planned for the campaign.",
    ),
    SchemaField(
        "planned_price",
        "Product price",
        "number",
        True,
        nullable=True,
        recommended_header="product_price",
        aliases=("product price", "product_price", "planned price", "price", "planned_price"),
        description="Campaign product price from the Excel plan.",
    ),
    SchemaField(
        "planned_category",
        "Planned category",
        "string",
        False,
        default="",
        recommended_header="planned_category",
        aliases=("category", "planned category", "planned_category"),
        description="Campaign category or placement.",
    ),
    SchemaField(
        "planned_visibility",
        "Planned visibility",
        "boolean",
        False,
        default=True,
        recommended_header="planned_visibility",
        aliases=("visibility", "planned visibility", "planned_visibility"),
        description="Whether the item should be visible in the target channel.",
    ),
    SchemaField(
        "planned_owner",
        "Planned owner",
        "string",
        False,
        default="",
        recommended_header="planned_owner",
        aliases=("owner", "planned owner", "planned_owner"),
        description="Person or team accountable for the campaign line.",
    ),
)

CHANNEL_ALIASES = {
    "webshop": "webshop",
    "web shop": "webshop",
    "online": "webshop",
    "b2b": "B2B",
    "mail order": "mail order",
    "mailorder": "mail order",
    "local store": "local store",
    "store": "local store",
}

REQUIRED_PLAN_COLUMNS = [field.name for field in CAMPAIGN_PLAN_SCHEMA if field.required]
OPTIONAL_PLAN_DEFAULTS = {
    field.name: field.default for field in CAMPAIGN_PLAN_SCHEMA if not field.required
}
PLAN_COLUMN_ALIASES = {
    alias: field.name
    for field in CAMPAIGN_PLAN_SCHEMA
    for alias in (field.name, *field.aliases)
}
PLAN_COLUMN_ORDER = [field.name for field in CAMPAIGN_PLAN_SCHEMA]


def _alias_key(value: object) -> str:
    raw = str(value).strip()
    normalized = raw.lower().replace("-", " ").replace("_", " ")
    return " ".join(normalized.split())


def canonical_column_name(name: object) -> str:
    raw = str(name).strip()
    return PLAN_COLUMN_ALIASES.get(_alias_key(raw), raw.lower().replace(" ", "_"))


def normalize_channel(value: object) -> str:
    if pd.isna(value):
        return ""
    raw = str(value).strip()
    return CHANNEL_ALIASES.get(raw.lower(), raw)


def _coerce_bool(value: object) -> bool:
    if pd.isna(value):
        return True
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"false", "no", "n", "0", "hidden"}:
        return False
    return True


def schema_as_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "column": field.name,
                "recommended_header": field.recommended_header or field.name,
                "label": field.label,
                "type": field.dtype,
                "required": field.required,
                "nullable": field.nullable,
                "aliases": ", ".join(field.aliases),
                "description": field.description,
            }
            for field in CAMPAIGN_PLAN_SCHEMA
        ]
    )


def campaign_plan_template() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "campaign_code": "CAMP-001",
                "campaign_name": "Summer Launch",
                "campaign_source": "Excel upload",
                "start_date": "2026-06-01",
                "end_date": "2026-06-14",
                "channel": "webshop",
                "product_sku": "SKU-001",
                "product_price": 19.90,
                "planned_category": "Summer Essentials",
                "planned_visibility": True,
                "planned_owner": "Alice (Campaigns)",
            }
        ],
        columns=[field.recommended_header or field.name for field in CAMPAIGN_PLAN_SCHEMA],
    )


def normalize_campaign_plan(
    plan: pd.DataFrame,
    default_source: str = "Uploaded file",
) -> tuple[pd.DataFrame | None, list[str]]:
    normalized = plan.copy()
    normalized.columns = [canonical_column_name(c) for c in normalized.columns]
    errors: list[str] = []

    duplicate_cols = normalized.columns[normalized.columns.duplicated()].unique().tolist()
    if duplicate_cols:
        errors.append(f"Duplicate columns after schema mapping: {', '.join(duplicate_cols)}")
        return None, errors

    missing = [col for col in REQUIRED_PLAN_COLUMNS if col not in normalized.columns]
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return None, errors

    for col, default in OPTIONAL_PLAN_DEFAULTS.items():
        if col not in normalized.columns:
            normalized[col] = default_source if col == "campaign_source" else default

    normalized = normalized[PLAN_COLUMN_ORDER].copy()

    if normalized.empty:
        errors.append("Uploaded campaign plan has no rows")
        return None, errors

    text_cols = [
        "campaign_id",
        "campaign_name",
        "campaign_source",
        "channel",
        "item_id",
        "planned_category",
        "planned_owner",
    ]
    for col in text_cols:
        normalized[col] = normalized[col].fillna("").astype(str).str.strip()

    normalized["campaign_source"] = normalized["campaign_source"].replace("", default_source)
    normalized["channel"] = normalized["channel"].apply(normalize_channel)
    normalized["planned_start"] = pd.to_datetime(normalized["planned_start"], errors="coerce")
    normalized["planned_end"] = pd.to_datetime(normalized["planned_end"], errors="coerce")
    normalized["planned_price"] = pd.to_numeric(normalized["planned_price"], errors="coerce")
    normalized["planned_visibility"] = normalized["planned_visibility"].apply(_coerce_bool)

    if normalized["planned_start"].isna().any():
        bad_rows = (normalized.index[normalized["planned_start"].isna()] + 2).tolist()
        errors.append(f"Invalid or missing planned_start on Excel row(s): {bad_rows}")
    if normalized["planned_end"].isna().any():
        bad_rows = (normalized.index[normalized["planned_end"].isna()] + 2).tolist()
        errors.append(f"Invalid or missing planned_end on Excel row(s): {bad_rows}")
    if normalized["campaign_id"].eq("").any():
        bad_rows = (normalized.index[normalized["campaign_id"].eq("")] + 2).tolist()
        errors.append(f"Empty campaign_id on Excel row(s): {bad_rows}")
    if normalized["campaign_name"].eq("").any():
        bad_rows = (normalized.index[normalized["campaign_name"].eq("")] + 2).tolist()
        errors.append(f"Empty campaign_name on Excel row(s): {bad_rows}")

    unknown_channels = sorted(
        ch for ch in normalized["channel"].dropna().unique()
        if ch and ch not in set(CHANNEL_ALIASES.values())
    )
    if unknown_channels:
        errors.append(f"Unknown channel value(s): {', '.join(unknown_channels)}")

    return (None if errors else normalized), errors
