"""Silver validation rules for machine_downtime (see docs/data_quality.md)."""

from pyspark.sql import functions as F


def missing_or_not_in(column, allowed):
    """Return a condition that is True when a value is NULL or not approved."""
    return F.col(column).isNull() | ~F.col(column).isin(allowed)


def plan_mismatch(expected_flags):
    """Return a condition that is True when planned_flag contradicts the reason."""
    condition = F.lit(False)
    for reason, expected in expected_flags.items():
        if expected == "any":
            continue
        opposite = "False" if expected == "True" else "True"
        condition = condition | (
            (F.col("downtime_reason") == reason) & (F.col("planned_flag") == opposite)
        )
    return condition


def machine_downtime_rules(reference):
    """Return the MD_ rules as (rule_id, reason, condition) triples."""
    return [
        (
            "MD_ID_MISSING",
            "Downtime event ID is missing",
            F.col("downtime_event_id").isNull()
            | (F.trim(F.col("downtime_event_id")) == ""),
        ),
        (
            "MD_MACHINE_UNKNOWN",
            "Machine is missing or not in the machine master",
            missing_or_not_in("machine_id", reference["machine_ids"]),
        ),
        (
            "MD_LINE_UNKNOWN",
            "Production line is missing or unknown",
            missing_or_not_in("production_line_id", reference["production_line_ids"]),
        ),
        (
            "MD_REASON_INVALID",
            "Downtime reason is missing or invalid",
            missing_or_not_in("downtime_reason", reference["downtime_reasons"]),
        ),
        (
            "MD_FLAG_INVALID",
            "Planned flag is missing or invalid",
            missing_or_not_in("planned_flag", reference["planned_flags"]),
        ),
        (
            "MD_TIME_MISSING",
            "Start or end time is missing",
            F.col("start_timestamp").isNull() | F.col("end_timestamp").isNull(),
        ),
        (
            "MD_TIME_ORDER",
            "End date is before start date",
            F.col("end_timestamp") < F.col("start_timestamp"),
        ),
        (
            "MD_LOSS_NEGATIVE",
            "Production loss cannot be negative",
            F.col("production_loss_units") < 0,
        ),
        (
            "MD_PLAN_MISMATCH",
            "Planned flag contradicts the downtime reason",
            plan_mismatch(reference["downtime_reason_planned_flag"]),
        ),
    ]
