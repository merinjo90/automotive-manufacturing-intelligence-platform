from src.generators.machine_downtime import (
    generate_machine_downtime,
    corrupt_negative_production_loss,
)


def test_generates_correct_number_of_records():
    records = generate_machine_downtime(50)
    assert len(records) == 50


def test_each_record_has_all_required_fields():
    records = generate_machine_downtime(10)
    expected_fields = {
        "downtime_event_id",
        "machine_id",
        "production_line_id",
        "start_timestamp",
        "end_timestamp",
        "downtime_reason",
        "planned_flag",
        "production_loss_units",
    }

    for record in records:
        assert set(record.keys()) == expected_fields


def test_corrupt_negative_production_loss_sets_negative_value():
    sample_record = {"production_loss_units": 0}
    corrupted = corrupt_negative_production_loss(sample_record)
    assert corrupted["production_loss_units"] < 0


def test_invalid_rate_is_roughly_five_percent():
    records = generate_machine_downtime(2000)

    def is_invalid(record):
        missing_id = record["downtime_event_id"] == ""
        negative_loss = record["production_loss_units"] < 0
        end_before_start = record["end_timestamp"] < record["start_timestamp"]
        return missing_id or negative_loss or end_before_start

    invalid_count = sum(1 for r in records if is_invalid(r))
    invalid_rate = invalid_count / len(records)

    assert 0.02 <= invalid_rate <= 0.08