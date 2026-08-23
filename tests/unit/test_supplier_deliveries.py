from src.generators.supplier_deliveries import generate_supplier_deliveries


def test_generates_correct_number_of_records():
    records = generate_supplier_deliveries(50)
    assert len(records) == 50


def test_each_record_has_all_required_fields():
    records = generate_supplier_deliveries(10)
    expected_fields = {
        "delivery_id",
        "supplier_id",
        "component_id",
        "plant_id",
        "purchase_order_id",
        "planned_delivery_date",
        "actual_delivery_date",
        "ordered_quantity",
        "delivered_quantity",
        "accepted_quantity",
        "rejected_quantity",
        "delivery_status",
    }

    for record in records:
        assert set(record.keys()) == expected_fields


def test_invalid_rate_is_roughly_five_percent():
    records = generate_supplier_deliveries(2000)

    def is_invalid(record):
        missing_id = record["delivery_id"] == ""
        bad_status = record["delivery_status"] == "UNKNOWN STATUS"
        mismatch = (
            record["accepted_quantity"] + record["rejected_quantity"]!= record["delivered_quantity"]
        )
        return missing_id or bad_status or mismatch

    invalid_count = sum(1 for r in records if is_invalid(r))
    invalid_rate = invalid_count / len(records)

    assert 0.02 <= invalid_rate <= 0.08