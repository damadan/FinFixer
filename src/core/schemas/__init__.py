"""Load JSON schemas for SGR sections."""

from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SCHEMA_NAMES = [
    "business_overview",
    "legal_structure",
    "financials",
    "legal_cases",
    "news",
    "assets_gallery",
    "container",
]

SCHEMAS: dict[str, dict] = {}
for name in SCHEMA_NAMES:
    with (BASE_DIR / f"{name}.schema.json").open(encoding="utf-8") as f:
        SCHEMAS[name] = json.load(f)

__all__ = ["SCHEMAS", "SCHEMA_NAMES"]
