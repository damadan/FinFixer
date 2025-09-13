from __future__ import annotations
import json
from importlib.resources import files
from typing import Dict, Any

# Разрешённые имена схем (для явной валидации)
SCHEMA_FILES = {
    "container": "container.schema.json",
    "business_overview": "business_overview.schema.json",
    "legal_structure": "legal_structure.schema.json",
    "financials": "financials.schema.json",
    "legal_cases": "legal_cases.schema.json",
    "news": "news.schema.json",
    "assets_gallery": "assets_gallery.schema.json",
}


def load_schema(name: str) -> Dict[str, Any]:
    """
    Возвращает JSON-схему по короткому имени (например, 'financials').
    """
    if name not in SCHEMA_FILES:
        raise KeyError(f"Unknown schema: {name}")
    path = files(__package__).joinpath(SCHEMA_FILES[name])
    return json.loads(path.read_text(encoding="utf-8"))
