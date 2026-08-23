from src.generators.quality_inspections import generate_quality_inspections


def test_generates_correct_number_of_records():
    records = generate_quality_inspections(50)
    assert len(records) == 50


def test_each_record_has_all_required_fields():
    records = generate_quality_inspections(10)
    expected_fields = {
        "inspection_id",
        "vehicle_id",
        "component_id",
        "supplier_id",
        "plant_id",
        "production_line_id",
        "inspection_timestamp",
        "inspection_result",
        "defect_code",
        "defect_severity",
        "rework_required",
        "scrap_required",
    }

    for record in records:
        assert set(record.keys()) == expected_fields


def test_pass_records_have_no_defect_info():
    records = generate_quality_inspections(500)

    for record in records:
        if record["inspection_result"] == "PASS" and record["component_id"] != "COMP999":
            assert record["defect_code"] == ""
            assert record["rework_required"] is False


def test_invalid_rate_is_roughly_five_percent():
    records = generate_quality_inspections(2000)

    def is_invalid(record):
        missing_id = record["inspection_id"] == ""
        bad_severity = record["defect_severity"] == "EXTREME"
        orphaned = record["component_id"] == "COMP999"
        return missing_id or bad_severity or orphaned

    invalid_count = sum(1 for r in records if is_invalid(r))
    invalid_rate = invalid_count / len(records)

    assert 0.02 <= invalid_rate <= 0.08