"""Unit tests for the explicit Bronze schemas."""

import csv

import pytest

from src.schemas.machine_downtime_schema import MACHINE_DOWNTIME_SCHEMA
from src.schemas.production_orders_schema import PRODUCTION_ORDERS_SCHEMA
from src.schemas.quality_inspections_schema import QUALITY_INSPECTIONS_SCHEMA
from src.schemas.supplier_deliveries_schema import SUPPLIER_DELIVERIES_SCHEMA

SCHEMAS = [
    ("supplier_deliveries", SUPPLIER_DELIVERIES_SCHEMA),
    ("production_orders", PRODUCTION_ORDERS_SCHEMA),
    ("quality_inspections", QUALITY_INSPECTIONS_SCHEMA),
    ("machine_downtime", MACHINE_DOWNTIME_SCHEMA),
]


@pytest.mark.parametrize("dataset, schema", SCHEMAS)
def test_schema_columns_match_sample_csv_header(dataset, schema):
    # Spark maps CSV columns by position, so the order must match.
    with open(f"data/sample/{dataset}.csv", newline="") as file:
        header = next(csv.reader(file))

    assert schema.fieldNames() == header


@pytest.mark.parametrize("dataset, schema", SCHEMAS)
def test_all_schema_fields_are_nullable(dataset, schema):
    # Bronze keeps raw rows; invalid values are rejected later in Silver.
    assert all(field.nullable for field in schema.fields)
