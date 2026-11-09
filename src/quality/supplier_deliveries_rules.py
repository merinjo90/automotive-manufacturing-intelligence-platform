"""Silver validation rules for supplier_deliveries (see docs/data_quality.md)."""

from pyspark.sql import functions as F

from src.quality.rules import (
    all_present_and_non_negative,
    any_missing,
    any_negative,
    missing_or_not_in,
)

QUANTITY_COLUMNS = [
    "ordered_quantity",
    "delivered_quantity",
    "accepted_quantity",
    "rejected_quantity",
]
MISMATCH_COLUMNS = ["delivered_quantity", "accepted_quantity", "rejected_quantity"]


def supplier_deliveries_rules(reference):
    """Return the SD_ rules as (rule_id, reason, condition) triples."""
    # Compare totals only when the quantities are valid, so one bad value fires one rule.
    quantities_valid = all_present_and_non_negative(MISMATCH_COLUMNS)
    return [
        (
            "SD_ID_MISSING",
            "Delivery ID is missing",
            F.col("delivery_id").isNull() | (F.trim(F.col("delivery_id")) == ""),
        ),
        (
            "SD_SUPPLIER_UNKNOWN",
            "Supplier is not in the supplier master",
            missing_or_not_in("supplier_id", reference["supplier_ids"]),
        ),
        (
            "SD_COMPONENT_UNKNOWN",
            "Component is not in the component master",
            missing_or_not_in("component_id", reference["component_ids"]),
        ),
        (
            "SD_PLANT_UNKNOWN",
            "Plant is missing or unknown",
            missing_or_not_in("plant_id", reference["plant_ids"]),
        ),
        (
            "SD_STATUS_INVALID",
            "Delivery status is not an approved value",
            missing_or_not_in("delivery_status", reference["delivery_statuses"]),
        ),
        (
            "SD_DATE_MISSING",
            "Planned or actual delivery date is missing",
            any_missing(["planned_delivery_date", "actual_delivery_date"]),
        ),
        (
            "SD_QTY_MISSING",
            "A quantity is missing",
            any_missing(QUANTITY_COLUMNS),
        ),
        (
            "SD_QTY_NEGATIVE",
            "A quantity is negative",
            any_negative(QUANTITY_COLUMNS),
        ),
        (
            "SD_QTY_MISMATCH",
            "Accepted plus rejected does not equal delivered",
            quantities_valid
            & (
                F.col("accepted_quantity") + F.col("rejected_quantity")
                != F.col("delivered_quantity")
            ),
        ),
    ]
