"""Integration tests for the supplier_deliveries Silver rules."""

from datetime import date

import pytest

from src.common.config import load_yaml
from src.quality.rules import add_failed_rules
from src.quality.supplier_deliveries_rules import supplier_deliveries_rules
from src.schemas.supplier_deliveries_schema import SUPPLIER_DELIVERIES_SCHEMA

REFERENCE_DATA = "configs/reference_data.yaml"

# Accepted plus rejected equals delivered, so every quantity rule passes.
VALID_ROW = {
    "delivery_id": "DEL001",
    "supplier_id": "SUP001",
    "component_id": "COMP001",
    "plant_id": "PLANT01",
    "purchase_order_id": "PO0001",
    "planned_delivery_date": date(2026, 3, 2),
    "actual_delivery_date": date(2026, 3, 4),
    "ordered_quantity": 1000,
    "delivered_quantity": 1000,
    "accepted_quantity": 950,
    "rejected_quantity": 50,
    "delivery_status": "LATE",
}


def failed_rules_for(spark, **changes):
    """Return the failed SD_ rule IDs for VALID_ROW with the given changes."""
    row = {**VALID_ROW, **changes}
    values = tuple(row[name] for name in SUPPLIER_DELIVERIES_SCHEMA.fieldNames())
    df = spark.createDataFrame([values], SUPPLIER_DELIVERIES_SCHEMA)
    rules = supplier_deliveries_rules(load_yaml(REFERENCE_DATA))
    return add_failed_rules(df, rules).first()["failed_rules"]


def test_valid_row_passes_every_rule(spark):
    assert failed_rules_for(spark) == []


@pytest.mark.parametrize(
    "changes, expected_rule",
    [
        ({"delivery_id": None}, "SD_ID_MISSING"),
        ({"delivery_id": "   "}, "SD_ID_MISSING"),
        ({"supplier_id": "SUP999"}, "SD_SUPPLIER_UNKNOWN"),
        ({"supplier_id": None}, "SD_SUPPLIER_UNKNOWN"),
        ({"component_id": "COMP999"}, "SD_COMPONENT_UNKNOWN"),
        ({"plant_id": "PLANT99"}, "SD_PLANT_UNKNOWN"),
        ({"delivery_status": "UNKNOWN STATUS"}, "SD_STATUS_INVALID"),
        ({"delivery_status": None}, "SD_STATUS_INVALID"),
        ({"planned_delivery_date": None}, "SD_DATE_MISSING"),
        ({"actual_delivery_date": None}, "SD_DATE_MISSING"),
        ({"ordered_quantity": None}, "SD_QTY_MISSING"),
        ({"rejected_quantity": None}, "SD_QTY_MISSING"),
        ({"accepted_quantity": -10}, "SD_QTY_NEGATIVE"),
        ({"accepted_quantity": 500, "rejected_quantity": 300}, "SD_QTY_MISMATCH"),
    ],
)
def test_each_rule_catches_its_invalid_value(spark, changes, expected_rule):
    assert failed_rules_for(spark, **changes) == [expected_rule]
