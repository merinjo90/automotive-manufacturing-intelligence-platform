import csv
from src.common.file_writers import write_records_to_csv

def test_write_records_to_csv_creates_correct_content(tmp_path):
    records = [
        {"delivery_id": "DE001", "supplier_id": "SUP001", "ordered_quantity": 1000},
    ]
    filepath = tmp_path/ "test_output.csv"

    write_records_to_csv(records,filepath)

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        row = list(reader)

    assert row[0]["delivery_id"] == "DE001"
    assert row[0]["supplier_id"] == "SUP001"