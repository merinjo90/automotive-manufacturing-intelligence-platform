from src.ingestion.file_tracker import (
    calculate_file_hash,
    load_tracking_log,
    was_file_processed,
)


def test_same_content_gives_same_hash(tmp_path):
    file_a = tmp_path / "a.csv"
    file_b = tmp_path / "b.csv"
    file_a.write_text("delivery_id\nDEL0001\n")
    file_b.write_text("delivery_id\nDEL0001\n")

    assert calculate_file_hash(file_a) == calculate_file_hash(file_b)


def test_changed_content_gives_different_hash(tmp_path):
    file_a = tmp_path / "a.csv"
    file_b = tmp_path / "b.csv"
    file_a.write_text("delivery_id\nDEL0001\n")
    file_b.write_text("delivery_id\nDEL0002\n")

    assert calculate_file_hash(file_a) != calculate_file_hash(file_b)


def test_hash_has_64_characters(tmp_path):
    file_a = tmp_path / "a.csv"
    file_a.write_text("delivery_id\nDEL0001\n")

    assert len(calculate_file_hash(file_a)) == 64


def test_missing_tracking_log_returns_empty_list(tmp_path):
    missing_log = tmp_path / "tracking.json"

    assert load_tracking_log(missing_log) == []


def test_existing_tracking_log_is_loaded(tmp_path):
    log_file = tmp_path / "tracking.json"
    log_file.write_text('[{"source_file": "a.csv", "file_hash": "abc123"}]')

    loaded = load_tracking_log(log_file)

    assert loaded == [{"source_file": "a.csv", "file_hash": "abc123"}]


def test_missing_log_means_file_not_processed(tmp_path):
    missing_log = tmp_path / "tracking.json"

    assert was_file_processed(missing_log, "abc123") is False


def test_hash_in_second_entry_is_found(tmp_path):
    log_file = tmp_path / "tracking.json"
    log_file.write_text('[{"file_hash": "xyz789"}, {"file_hash": "abc123"}]')

    assert was_file_processed(log_file, "abc123") is True


def test_same_name_with_new_hash_is_not_processed(tmp_path):
    log_file = tmp_path / "tracking.json"
    log_file.write_text('[{"source_file": "a.csv", "file_hash": "xyz789"}]')

    assert was_file_processed(log_file, "abc123") is False
