"""Integration tests for the machine_downtime Silver rules."""

from datetime import date

import pytest

from src.common.config import load_yaml
from src.quality.machine_downtime_rules import machine_downtime_rules
from src.quality.rules import add_failed_rules
from src.schemas.machine_downtime_schema import MACHINE_DOWNTIME_SCHEMA

REFERENCE_DATA = "configs/reference_data.yaml"

# Same-day start and end is valid: the data has date precision only.
VALID_ROW = {
    "downtime_event_id": "DT001",
    "machine_id": "MACH001",
    "production_line_id": "LINE01",
    "start_timestamp": date(2026, 3, 2),
    "end_timestamp": date(2026, 3, 2),
    "downtime_reason": "MECHANICAL_FAILURE",
    "planned_flag": "False",
    "production_loss_units": 40,
}


def failed_rules_for(spark, **changes):
    row = {**VALID_ROW, **changes}
    values = tuple(row[name] for name in MACHINE_DOWNTIME_SCHEMA.fieldNames())
    df = spark.createDataFrame([values], MACHINE_DOWNTIME_SCHEMA)
    rules = machine_downtime_rules(load_yaml(REFERENCE_DATA))
    return add_failed_rules(df, rules).first()["failed_rules"]


def test_valid_row_passes_every_rule(spark):
    assert failed_rules_for(spark) == []


@pytest.mark.parametrize(
    "changes, expected_rule",
    [
        ({"downtime_event_id": None}, "MD_ID_MISSING"),
        ({"downtime_event_id": "   "}, "MD_ID_MISSING"),
        ({"machine_id": "MACH009"}, "MD_MACHINE_UNKNOWN"),
        ({"machine_id": None}, "MD_MACHINE_UNKNOWN"),
        ({"production_line_id": "LINE99"}, "MD_LINE_UNKNOWN"),
        ({"downtime_reason": "UNKNOWN"}, "MD_REASON_INVALID"),
        ({"planned_flag": "Maybe"}, "MD_FLAG_INVALID"),
        ({"start_timestamp": None}, "MD_TIME_MISSING"),
        ({"end_timestamp": date(2026, 3, 1)}, "MD_TIME_ORDER"),
        ({"production_loss_units": -20}, "MD_LOSS_NEGATIVE"),
        ({"planned_flag": "True"}, "MD_PLAN_MISMATCH"),
        (
            {"downtime_reason": "SCHEDULED_MAINTENANCE", "planned_flag": "False"},
            "MD_PLAN_MISMATCH",
        ),
    ],
)
def test_each_rule_catches_its_invalid_value(spark, changes, expected_rule):
    assert failed_rules_for(spark, **changes) == [expected_rule]
