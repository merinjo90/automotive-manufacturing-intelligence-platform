from datetime import date
import random

from src.common.date_helpers import generate_random_date
from src.common.file_writers import write_records_to_csv
from src.common.data_quality import should_create_invalid_record

SUPPLIER_IDS = ["SUP001", "SUP002", "SUP003"]
COMPONENT_IDS = ["COMP001", "COMP002", "COMP003"]
PLANT_IDS = ["PLANT01", "PLANT02"]


def generate_supplier_deliveries(num_records):
    records = []

    for i in range(num_records):
        planned_date = generate_random_date(date(2026, 1, 1), 30)
        actual_date = generate_random_date(planned_date, 10)

        ordered_quantity = 1000
        rejected_quantity = 50

        if should_create_invalid_record(0.05):
            rejected_quantity = -50

        record = {
            "delivery_id": f"DEL{i:04d}",
            "supplier_id": random.choice(SUPPLIER_IDS),
            "component_id": random.choice(COMPONENT_IDS),
            "plant_id": random.choice(PLANT_IDS),
            "purchase_order_id": f"PO{i:04d}",
            "planned_delivery_date": planned_date,
            "actual_delivery_date": actual_date,
            "ordered_quantity": 1000,
            "delivered_quantity": 1000,
            "accepted_quantity": 950,
            "rejected_quantity": rejected_quantity,
            "delivery_status": "LATE",
        }
        records.append(record)

    return records