from __future__ import annotations

from pathlib import Path
import sys

import jsonschema
import pytest

# allow importing from src
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from core.schemas import SCHEMAS  # noqa: E402

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "src" / "core" / "schemas"


def _resolver(name: str) -> jsonschema.RefResolver:
    schema_path = SCHEMA_DIR / f"{name}.schema.json"
    return jsonschema.RefResolver(base_uri=schema_path.as_uri(), referrer=SCHEMAS[name])


FORMAT_CHECKER = jsonschema.FormatChecker()


EXAMPLES = {
    "business_overview": {
        "valid": [
            {
                "company_name": "ABC Ltd",
                "inn": "1234567890",
                "ogrn": "1234567890123",
                "registration_date": "2020-01-01",
                "source": "registry",
                "confidence": 0.9,
            },
            {
                "company_name": "XYZ LLC",
                "inn": "9876543210",
                "ogrn": "9876543210987",
                "registration_date": "2021-12-31",
                "source": "registry",
                "confidence": 0.8,
            },
            {
                "company_name": "Foo Bar",
                "inn": "1020304050",
                "ogrn": "1231231231231",
                "registration_date": "2022-05-20",
                "source": "manual",
                "confidence": 1,
            },
        ],
        "invalid": [
            {
                "company_name": "Bad Inn",
                "inn": "12345",
                "ogrn": "1234567890123",
                "registration_date": "2020-01-01",
                "source": "registry",
                "confidence": 0.9,
            },
            {
                "company_name": "Missing OGRN",
                "inn": "1234567890",
                "registration_date": "2020-01-01",
                "source": "registry",
                "confidence": 0.9,
            },
            {
                "company_name": "Bad Date",
                "inn": "1234567890",
                "ogrn": "1234567890123",
                "registration_date": "01-01-2020",
                "source": "registry",
                "confidence": 0.9,
            },
        ],
    },
    "legal_structure": {
        "valid": [
            {
                "owners": [
                    {"name": "Owner1", "share": 60},
                    {"name": "Owner2", "share": 40},
                ],
                "source": "statements",
                "confidence": 0.7,
            },
            {
                "owners": [{"name": "Owner", "share": 100}],
                "source": "statements",
                "confidence": 1,
            },
            {
                "owners": [
                    {"name": "A", "share": 33.3},
                    {"name": "B", "share": 66.7},
                ],
                "source": "registry",
                "confidence": 0.5,
            },
        ],
        "invalid": [
            {
                "owners": [{"name": "Owner1", "share": 150}],
                "source": "statements",
                "confidence": 0.7,
            },
            {
                "owners": [{"share": 50}],
                "source": "statements",
                "confidence": 0.7,
            },
            {
                "source": "statements",
                "confidence": 0.7,
            },
        ],
    },
    "financials": {
        "valid": [
            {
                "revenue": 1000,
                "profit": 100,
                "reporting_date": "2023-12-31",
                "source": "report",
                "confidence": 0.9,
            },
            {
                "revenue": 0,
                "profit": 0,
                "reporting_date": "2022-06-30",
                "source": "report",
                "confidence": 0.8,
            },
            {
                "revenue": 500,
                "profit": -50,
                "reporting_date": "2021-01-01",
                "source": "audit",
                "confidence": 0.6,
            },
        ],
        "invalid": [
            {
                "revenue": -1,
                "profit": 10,
                "reporting_date": "2023-12-31",
                "source": "report",
                "confidence": 0.9,
            },
            {
                "revenue": 100,
                "profit": 10,
                "source": "report",
                "confidence": 0.9,
            },
            {
                "revenue": 100,
                "profit": 10,
                "reporting_date": "31-12-2023",
                "source": "report",
                "confidence": 0.9,
            },
        ],
    },
    "legal_cases": {
        "valid": [
            {
                "cases": [
                    {
                        "case_number": "A1",
                        "decision_date": "2023-03-01",
                        "status": "open",
                    }
                ],
                "source": "courts",
                "confidence": 0.4,
            },
            {
                "cases": [
                    {
                        "case_number": "B2",
                        "decision_date": "2020-11-15",
                        "status": "closed",
                    }
                ],
                "source": "courts",
                "confidence": 0.8,
            },
            {
                "cases": [
                    {
                        "case_number": "C3",
                        "decision_date": "2022-07-07",
                        "status": "open",
                    },
                    {
                        "case_number": "D4",
                        "decision_date": "2021-05-05",
                        "status": "closed",
                    },
                ],
                "source": "courts",
                "confidence": 0.9,
            },
        ],
        "invalid": [
            {
                "cases": [
                    {
                        "case_number": "E5",
                        "decision_date": "2023-01-01",
                        "status": "pending",
                    }
                ],
                "source": "courts",
                "confidence": 0.5,
            },
            {
                "cases": [{"decision_date": "2023-01-01", "status": "open"}],
                "source": "courts",
                "confidence": 0.5,
            },
            {
                "source": "courts",
                "confidence": 0.5,
            },
        ],
    },
    "news": {
        "valid": [
            {
                "items": [{"headline": "News 1", "date": "2023-01-01"}],
                "source": "media",
                "confidence": 0.7,
            },
            {
                "items": [
                    {"headline": "News 2", "date": "2022-12-12"},
                    {"headline": "News 3", "date": "2022-12-13"},
                ],
                "source": "media",
                "confidence": 0.6,
            },
            {
                "items": [{"headline": "Another", "date": "2020-05-05"}],
                "source": "media",
                "confidence": 1,
            },
        ],
        "invalid": [
            {
                "items": [{"date": "2023-01-01"}],
                "source": "media",
                "confidence": 0.7,
            },
            {
                "items": [{"headline": "Bad Date", "date": "01-01-2023"}],
                "source": "media",
                "confidence": 0.7,
            },
            {
                "source": "media",
                "confidence": 0.7,
            },
        ],
    },
    "assets_gallery": {
        "valid": [
            {
                "assets": [
                    {
                        "description": "Car",
                        "url": "http://example.com/car.jpg",
                        "valuation": 10000,
                    }
                ],
                "source": "inventory",
                "confidence": 0.9,
            },
            {
                "assets": [
                    {
                        "description": "House",
                        "url": "https://example.com/house.png",
                    }
                ],
                "source": "inventory",
                "confidence": 0.8,
            },
            {
                "assets": [
                    {
                        "description": "Boat",
                        "url": "http://example.com/boat.jpg",
                        "valuation": 0,
                    }
                ],
                "source": "inventory",
                "confidence": 0.6,
            },
        ],
        "invalid": [
            {
                "assets": [{"description": "Car", "valuation": 10000}],
                "source": "inventory",
                "confidence": 0.9,
            },
            {
                "assets": [
                    {
                        "description": "Car",
                        "url": "http://example.com/car.jpg",
                        "valuation": -100,
                    }
                ],
                "source": "inventory",
                "confidence": 0.9,
            },
            {
                "source": "inventory",
                "confidence": 0.9,
            },
        ],
    },
}

# build container examples using previous ones
EXAMPLES["container"] = {
    "valid": [
        {
            "business_overview": EXAMPLES["business_overview"]["valid"][0],
            "legal_structure": EXAMPLES["legal_structure"]["valid"][0],
            "financials": EXAMPLES["financials"]["valid"][0],
            "legal_cases": EXAMPLES["legal_cases"]["valid"][0],
            "news": EXAMPLES["news"]["valid"][0],
            "assets_gallery": EXAMPLES["assets_gallery"]["valid"][0],
            "source": "container",
            "confidence": 0.9,
        },
        {
            "business_overview": EXAMPLES["business_overview"]["valid"][1],
            "legal_structure": EXAMPLES["legal_structure"]["valid"][1],
            "financials": EXAMPLES["financials"]["valid"][1],
            "legal_cases": EXAMPLES["legal_cases"]["valid"][1],
            "news": EXAMPLES["news"]["valid"][1],
            "assets_gallery": EXAMPLES["assets_gallery"]["valid"][1],
            "source": "container",
            "confidence": 0.8,
        },
        {
            "business_overview": EXAMPLES["business_overview"]["valid"][2],
            "legal_structure": EXAMPLES["legal_structure"]["valid"][2],
            "financials": EXAMPLES["financials"]["valid"][2],
            "legal_cases": EXAMPLES["legal_cases"]["valid"][2],
            "news": EXAMPLES["news"]["valid"][2],
            "assets_gallery": EXAMPLES["assets_gallery"]["valid"][2],
            "source": "container",
            "confidence": 1,
        },
    ],
    "invalid": [
        {
            # missing news
            "business_overview": EXAMPLES["business_overview"]["valid"][0],
            "legal_structure": EXAMPLES["legal_structure"]["valid"][0],
            "financials": EXAMPLES["financials"]["valid"][0],
            "legal_cases": EXAMPLES["legal_cases"]["valid"][0],
            "assets_gallery": EXAMPLES["assets_gallery"]["valid"][0],
            "source": "container",
            "confidence": 0.9,
        },
        {
            # invalid business_overview
            "business_overview": EXAMPLES["business_overview"]["invalid"][0],
            "legal_structure": EXAMPLES["legal_structure"]["valid"][0],
            "financials": EXAMPLES["financials"]["valid"][0],
            "legal_cases": EXAMPLES["legal_cases"]["valid"][0],
            "news": EXAMPLES["news"]["valid"][0],
            "assets_gallery": EXAMPLES["assets_gallery"]["valid"][0],
            "source": "container",
            "confidence": 0.9,
        },
        {
            # confidence out of range
            "business_overview": EXAMPLES["business_overview"]["valid"][0],
            "legal_structure": EXAMPLES["legal_structure"]["valid"][0],
            "financials": EXAMPLES["financials"]["valid"][0],
            "legal_cases": EXAMPLES["legal_cases"]["valid"][0],
            "news": EXAMPLES["news"]["valid"][0],
            "assets_gallery": EXAMPLES["assets_gallery"]["valid"][0],
            "source": "container",
            "confidence": 1.5,
        },
    ],
}


@pytest.mark.parametrize(
    "schema_name, example",
    [(name, ex) for name, data in EXAMPLES.items() for ex in data["valid"]],
)
def test_valid_examples(schema_name: str, example: dict) -> None:
    resolver = _resolver(schema_name)
    jsonschema.validate(
        example,
        SCHEMAS[schema_name],
        resolver=resolver,
        format_checker=FORMAT_CHECKER,
    )


@pytest.mark.parametrize(
    "schema_name, example",
    [(name, ex) for name, data in EXAMPLES.items() for ex in data["invalid"]],
)
def test_invalid_examples(schema_name: str, example: dict) -> None:
    resolver = _resolver(schema_name)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            example,
            SCHEMAS[schema_name],
            resolver=resolver,
            format_checker=FORMAT_CHECKER,
        )
