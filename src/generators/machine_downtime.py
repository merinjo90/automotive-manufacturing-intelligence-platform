from datetime import date, timedelta
import random

from src.common.date_helpers import generate_random_date
from src.common.data_quality import should_create_invalid_record

MACHINE_IDS = ["MACH001", "MACH002", "MACH003"]
PRODUCTION_LINE_IDS = ["LINE01", "LINE02", "LINE03"]
DOWNTIME_REASONS = ["MECHANICAL_FAILURE", "ELECTRICAL_FAULT", "SCHEDULED_MAINTENANCE"]


def corrupt_missing_downtime_event_id(record):
    record["downtime_event_id"] = ""
    return record


def corrupt_negative_production_loss(record):
    record["production_loss_units"] = -20
    return record


def corrupt_end_before_start(record):
    original_start = record["start_timestamp"]
    record["end_timestamp"] = original_start
    record["start_timestamp"] = original_start + timedelta(days=random.randint(1, 3))
    return record


def generate_machine_downtime(num_records):
    records = []

    for i in range(num_records):
        start = generate_random_date(date(2026, 1, 1), 60)
        end = generate_random_date(start, 2)
        is_planned = random.choice([True, False])

        record = {
            "downtime_event_id": f"DOWN{i:04d}",
            "machine_id": random.choice(MACHINE_IDS),
            "production_line_id": random.choice(PRODUCTION_LINE_IDS),
            "start_timestamp": start,
            "end_timestamp": end,
            "downtime_reason": "SCHEDULED_MAINTENANCE" if is_planned else random.choice(DOWNTIME_REASONS),
            "planned_flag": is_planned,
            "production_loss_units": 0 if is_planned else 50,
        }

        if should_create_invalid_record(0.05):
            corruption_functions = [
                corrupt_missing_downtime_event_id,
                corrupt_negative_production_loss,
                corrupt_end_before_start,
            ]
            chosen_corruption = random.choice(corruption_functions)
            record = chosen_corruption(record)

        records.append(record)

    return records