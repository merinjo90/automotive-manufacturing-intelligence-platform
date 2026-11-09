"""Integration tests for the production_orders Silver rules."""

from datetime import date

import pytest

from src.common.config import load_yaml
from src.quality.production_orders_rules import production_orders_rules
from src.quality.rules import add_failed_rules
from src.schemas.production_orders_schema import PRODUCTION_ORDERS_SCHEMA

REFERENCE_DATA = "configs/reference_data.yaml"

# A finished order: every time and quantity present, rework plus scrap within actual.
VALID_ROW = {
    "production_order_id": "PO0001",
    "vehicle_model_id": "MODEL_A",
    "plant_id": "PLANT01",
    "production_line_id": "LINE01",
    "planned_start_time": date(2026, 3, 2),
    "actual_start_time": date(2026, 3, 3),
    "planned_end_time": date(2026, 3, 6),
    "actual_end_time": date(2026, 3, 6),
    "planned_quantity": 100,
    "actual_quantity": 95,
    "rework_quantity": 3,
    "scrap_quantity": 2,
    "production_status": "COMPLETED",
}


def failed_rules_for(spark, **changes):
    """Return the failed PO_ rule IDs for VALID_ROW with the given changes."""
    row = {**VALID_ROW, **changes}
    values = tuple(row[name] for name in PRODUCTION_ORDERS_SCHEMA.fieldNames())
    df = spark.createDataFrame([values], PRODUCTION_ORDERS_SCHEMA)
    rules = production_orders_rules(load_yaml(REFERENCE_DATA))
    return add_failed_rules(df, rules).first()["failed_rules"]


def test_valid_row_passes_every_rule(spark):
    assert failed_rules_for(spark) == []


@pytest.mark.parametrize(
    "changes, expected_rule",
    [
        ({"production_order_id": None}, "PO_ID_MISSING"),
        ({"production_order_id": ""}, "PO_ID_MISSING"),
        ({"production_order_id": "   "}, "PO_ID_MISSING"),
        ({"vehicle_model_id": "MODEL_Z"}, "PO_MODEL_UNKNOWN"),
        ({"vehicle_model_id": None}, "PO_MODEL_UNKNOWN"),
        ({"plant_id": "PLANT99"}, "PO_PLANT_UNKNOWN"),
        ({"production_line_id": "LINE99"}, "PO_LINE_UNKNOWN"),
        ({"production_status": "UNKNOWN_STATUS"}, "PO_STATUS_INVALID"),
        ({"production_status": None}, "PO_STATUS_INVALID"),
    ],
)
def test_one_problem_fires_one_rule(spark, changes, expected_rule):
    assert failed_rules_for(spark, **changes) == [expected_rule]
