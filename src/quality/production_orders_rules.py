"""Silver validation rules for production_orders (see docs/data_quality.md)."""

from pyspark.sql import functions as F

from src.quality.rules import missing_or_not_in


def production_orders_rules(reference):
    """Return the PO_ rules as (rule_id, reason, condition) triples."""
    return [
        (
            "PO_ID_MISSING",
            "Production order ID is missing",
            F.col("production_order_id").isNull()
            | (F.trim(F.col("production_order_id")) == ""),
        ),
        (
            "PO_MODEL_UNKNOWN",
            "Vehicle model is missing or unknown",
            missing_or_not_in("vehicle_model_id", reference["vehicle_model_ids"]),
        ),
        (
            "PO_PLANT_UNKNOWN",
            "Plant is missing or unknown",
            missing_or_not_in("plant_id", reference["plant_ids"]),
        ),
        (
            "PO_LINE_UNKNOWN",
            "Production line is missing or unknown",
            missing_or_not_in("production_line_id", reference["production_line_ids"]),
        ),
        (
            "PO_STATUS_INVALID",
            "Production status is missing or invalid",
            missing_or_not_in("production_status", reference["production_statuses"]),
        ),
    ]
