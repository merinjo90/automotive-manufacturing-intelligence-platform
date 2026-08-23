from src.generators.production_orders import generate_production_orders


def test_generates_correct_number_of_records():
    records = generate_production_orders(50)
    assert len(records) == 50


def test_each_record_has_all_required_fields():
    records = generate_production_orders(10)
    expected_fields = {
        "production_order_id",
        "vehicle_model_id",
        "plant_id",
        "production_line_id",
        "planned_start_time",
        "actual_start_time",
        "planned_end_time",
        "actual_end_time",
        "planned_quantity",
        "actual_quantity",
        "rework_quantity",
        "scrap_quantity",
        "production_status",
    }

    for record in records:
        assert set(record.keys()) == expected_fields


def test_actual_end_is_never_before_actual_start():
    records = generate_production_orders(500)

    for record in records:
        assert record["actual_end_time"] >= record["actual_start_time"]


def test_invalid_rate_is_roughly_five_percent():
    records = generate_production_orders(2000)

    def is_invalid(record):
        missing_id = record["production_order_id"] == ""
        bad_status = record["production_status"] == "UNKNOWN_STATUS"
        negative_scrap = record["scrap_quantity"] < 0
        return missing_id or bad_status or negative_scrap

    invalid_count = sum(1 for r in records if is_invalid(r))
    invalid_rate = invalid_count / len(records)

    assert 0.02 <= invalid_rate <= 0.08