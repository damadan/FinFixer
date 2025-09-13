from __future__ import annotations

from pathlib import Path
import sys

import jsonschema
import pytest

# allow importing from src
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from core.schemas import load_schema  # noqa: E402

FORMAT_CHECKER = jsonschema.FormatChecker()

BUSINESS_OVERVIEW_VALID = {
    "text": "Some overview",
    "sources": ["https://example.com"],
    "confidence": 0.9,
}
BUSINESS_OVERVIEW_INVALID = {
    "text": "Bad confidence",
    "sources": ["https://example.com"],
    "confidence": 2,
}

LEGAL_STRUCTURE_VALID = {
    "nodes": [
        {
            "id": "n1",
            "type": "HoldCo",
            "label": "HoldCo LLC",
            "inn": "1234567890",
            "ogrn": "1234567890123",
            "status": None,
        },
        {"id": "n2", "type": "OpCo", "label": "OpCo LLC"},
    ],
    "edges": [{"from": "n1", "to": "n2", "relation": "owns", "share": 100}],
    "sources": ["https://example.com"],
    "confidence": 0.8,
}
LEGAL_STRUCTURE_INVALID = {
    "nodes": [
        {
            "id": "n1",
            "type": "HoldCo",
            "label": "HoldCo LLC",
            "inn": "1234",
        }
    ],
    "edges": [],
    "sources": ["https://example.com"],
    "confidence": 0.8,
}

FINANCIALS_VALID = [
    {
        "period": "FY2023",
        "currency": "USD",
        "pnl": {
            "revenue": 100,
            "cogs": 50,
            "gross_profit": 50,
            "opex": 10,
            "ebit": 40,
            "net_income": 30,
        },
        "bs": {
            "total_assets": 200,
            "inventory": 10,
            "receivables": 20,
            "payables": 15,
            "cash": 5,
            "st_debt": 0,
            "lt_debt": 0,
            "current_assets": 50,
            "current_liabilities": 20,
        },
        "cf": {
            "cfo": 40,
            "cfi": -10,
            "cff": 0,
            "ending_cash": 5,
        },
        "derived": {
            "net_debt": -5,
            "nwc": 30,
            "inv_days": 10,
            "ar_days": 20,
            "ap_days": 30,
            "ebit_margin": 0.4,
            "net_margin": 0.3,
        },
        "source": "https://example.com/fin",
        "confidence": 0.9,
    }
]
FINANCIALS_INVALID = [
    {
        "period": "FY2023",
        "currency": "US",
        "pnl": {
            "revenue": 100,
            "cogs": 50,
            "gross_profit": 50,
            "opex": 10,
            "ebit": 40,
            "net_income": 30,
        },
        "bs": {
            "total_assets": 200,
            "inventory": 10,
            "receivables": 20,
            "payables": 15,
            "cash": 5,
            "st_debt": 0,
            "lt_debt": 0,
            "current_assets": 50,
            "current_liabilities": 20,
        },
        "cf": {
            "cfo": 40,
            "cfi": -10,
            "cff": 0,
            "ending_cash": 5,
        },
        "derived": {
            "net_debt": -5,
            "nwc": 30,
            "inv_days": 10,
            "ar_days": 20,
            "ap_days": 30,
            "ebit_margin": 0.4,
            "net_margin": 0.3,
        },
        "source": "https://example.com/fin",
        "confidence": 0.9,
    }
]

LEGAL_CASES_VALID = [
    {
        "case_id": "1",
        "court": "Court",
        "date": "2024-01-01",
        "role": "plaintiff",
        "subject": "Subject",
        "stage": "ongoing",
        "amount": 1000,
        "url": "https://example.com/case",
        "confidence": 0.9,
    }
]
LEGAL_CASES_INVALID = [
    {
        "case_id": "1",
        "court": "Court",
        "date": "2024-01-01",
        "role": "owner",
        "subject": "Subject",
        "stage": "ongoing",
        "url": "https://example.com/case",
        "confidence": 0.9,
    }
]

NEWS_VALID = [
    {
        "date": "2024-01-01",
        "title": "Title",
        "category": "incident",
        "url": "https://example.com/news",
        "summary": "Summary",
        "confidence": 0.5,
    }
]
NEWS_INVALID = [
    {
        "date": "2024-01-01",
        "title": "Title",
        "category": "unknown",
        "url": "https://example.com/news",
        "summary": "Summary",
        "confidence": 0.5,
    }
]

ASSETS_GALLERY_VALID = [
    {
        "caption": "Photo",
        "url": "https://example.com/photo.jpg",
        "taken_at": None,
        "license": None,
    }
]
ASSETS_GALLERY_INVALID = [{"caption": "Photo"}]

CONTAINER_VALID = {
    "company_id": "comp1",
    "resolved": {
        "inn": "1234567890",
        "ogrn": "1234567890123",
        "names": ["Name LLC"],
        "website": "https://example.com",
    },
    "sections": {
        "business_overview": BUSINESS_OVERVIEW_VALID,
        "legal_structure": LEGAL_STRUCTURE_VALID,
        "financials": FINANCIALS_VALID,
        "legal_cases": LEGAL_CASES_VALID,
        "news": NEWS_VALID,
        "assets_gallery": ASSETS_GALLERY_VALID,
    },
}
CONTAINER_INVALID = [
    {
        "company_id": "comp1",
        "resolved": {
            "inn": "123",
            "ogrn": "1234567890123",
            "names": ["Name LLC"],
            "website": "https://example.com",
        },
        "sections": {
            "business_overview": BUSINESS_OVERVIEW_VALID,
            "legal_structure": LEGAL_STRUCTURE_VALID,
            "financials": FINANCIALS_VALID,
            "legal_cases": LEGAL_CASES_VALID,
            "news": NEWS_VALID,
            "assets_gallery": ASSETS_GALLERY_VALID,
        },
    },
    {
        "company_id": "comp1",
        "resolved": {
            "inn": "1234567890",
            "ogrn": "1234567890123",
            "names": ["Name LLC"],
            "website": "https://example.com",
        },
        "sections": {
            "business_overview": BUSINESS_OVERVIEW_VALID,
            "legal_structure": LEGAL_STRUCTURE_VALID,
            "financials": FINANCIALS_VALID,
            "legal_cases": LEGAL_CASES_VALID,
            "assets_gallery": ASSETS_GALLERY_VALID,
        },
    },
]

EXAMPLES = {
    "business_overview": {
        "valid": [BUSINESS_OVERVIEW_VALID],
        "invalid": [BUSINESS_OVERVIEW_INVALID],
    },
    "legal_structure": {
        "valid": [LEGAL_STRUCTURE_VALID],
        "invalid": [LEGAL_STRUCTURE_INVALID],
    },
    "financials": {"valid": [FINANCIALS_VALID], "invalid": [FINANCIALS_INVALID]},
    "legal_cases": {"valid": [LEGAL_CASES_VALID], "invalid": [LEGAL_CASES_INVALID]},
    "news": {"valid": [NEWS_VALID], "invalid": [NEWS_INVALID]},
    "assets_gallery": {
        "valid": [ASSETS_GALLERY_VALID],
        "invalid": [ASSETS_GALLERY_INVALID],
    },
    "container": {"valid": [CONTAINER_VALID], "invalid": CONTAINER_INVALID},
}


@pytest.mark.parametrize(
    "schema_name, example",
    [(name, ex) for name, data in EXAMPLES.items() for ex in data["valid"]],
)
def test_valid_examples(schema_name: str, example: dict) -> None:
    schema = load_schema(schema_name)
    jsonschema.validate(example, schema, format_checker=FORMAT_CHECKER)


@pytest.mark.parametrize(
    "schema_name, example",
    [(name, ex) for name, data in EXAMPLES.items() for ex in data["invalid"]],
)
def test_invalid_examples(schema_name: str, example: dict) -> None:
    schema = load_schema(schema_name)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(example, schema, format_checker=FORMAT_CHECKER)
