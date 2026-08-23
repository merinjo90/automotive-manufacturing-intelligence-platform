from datetime import date
import random

from src.common.date_helpers import generate_random_date
from src.common.data_quality import should_create_invalid_record

VEHICLE_MODEL_IDS = ["MODEL_A", "MODEL_B", "MODEL_C"]
PLANT_IDS = ["PLANT01", "PLANT02"]
PRODUCTION_LINE_IDS = ["LINE01", "LINE02", "LINE03"]


def corrupt_missing_production_order_id(record):
    record["production_order_id"] = ""
    return record


def corrupt_invalid_status(record):
    record["production_status"] = "UNKNOWN_STATUS"
    return record


def corrupt_negative_scrap(record):
    record["scrap_quantity"] = -10
    return record


def generate_production_orders(num_records):
    records = []

    for i in range(num_records):
        # NOTE: planned/actual _time fields currently store date-only
        # precision (no hour/minute). Full timestamp support is a
        # documented future improvement (see ADR).
        planned_start = generate_random_date(date(2026, 1, 1), 30)
        actual_start = generate_random_date(planned_start, 3)
        planned_end = generate_random_date(planned_start, 5)
        actual_end = generate_random_date(actual_start, 5)

        record = {
            "production_order_id": f"PROD{i:04d}",
            "vehicle_model_id": random.choice(VEHICLE_MODEL_IDS),
            "plant_id": random.choice(PLANT_IDS),
            "production_line_id": random.choice(PRODUCTION_LINE_IDS),
            "planned_start_time": planned_start,
            "actual_start_time": actual_start,
            "planned_end_time": planned_end,
            "actual_end_time": actual_end,
            "planned_quantity": 500,
            "actual_quantity": 480,
            "rework_quantity": 15,
            "scrap_quantity": 5,
            "production_status": "COMPLETED",
        }

        if should_create_invalid_record(0.05):
            corruption_functions = [
                corrupt_missing_production_order_id,
                corrupt_invalid_status,
                corrupt_negative_scrap,
            ]
            chosen_corruption = random.choice(corruption_functions)
            record = chosen_corruption(record)

        records.append(record)

    return records