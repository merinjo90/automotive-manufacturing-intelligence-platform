from datetime import date
import random

from src.common.date_helpers import generate_random_date
from src.common.data_quality import should_create_invalid_record

VEHICLE_IDS = ["VEH001", "VEH002", "VEH003"]
COMPONENT_IDS = ["COMP001", "COMP002", "COMP003"]
SUPPLIER_IDS = ["SUP001", "SUP002", "SUP003"]
PLANT_IDS = ["PLANT01", "PLANT02"]
PRODUCTION_LINE_IDS = ["LINE01", "LINE02", "LINE03"]
DEFECT_CODES = ["SCRATCH", "DIMENSION_ERROR", "ELECTRICAL_FAULT"]


def corrupt_missing_inspection_id(record):
    record["inspection_id"] = ""
    return record


def corrupt_invalid_defect_severity(record):
    record["defect_severity"] = "EXTREME"
    return record


def corrupt_orphaned_component(record):
    record["component_id"] = "COMP999"
    return record


def generate_quality_inspections(num_records):
    records = []

    for i in range(num_records):
        inspection_date = generate_random_date(date(2026, 1, 1), 60)
        is_defect = random.choice([True, False])

        record = {
            "inspection_id": f"INSP{i:04d}",
            "vehicle_id": random.choice(VEHICLE_IDS),
            "component_id": random.choice(COMPONENT_IDS),
            "supplier_id": random.choice(SUPPLIER_IDS),
            "plant_id": random.choice(PLANT_IDS),
            "production_line_id": random.choice(PRODUCTION_LINE_IDS),
            "inspection_timestamp": inspection_date,
            "inspection_result": "FAIL" if is_defect else "PASS",
            "defect_code": random.choice(DEFECT_CODES) if is_defect else "",
            "defect_severity": "MINOR" if is_defect else "",
            "rework_required": is_defect,
            "scrap_required": False,
        }

        if should_create_invalid_record(0.05):
            corruption_functions = [
                corrupt_missing_inspection_id,
                corrupt_invalid_defect_severity,
                corrupt_orphaned_component,
            ]
            chosen_corruption = random.choice(corruption_functions)
            record = chosen_corruption(record)

        records.append(record)

    return records