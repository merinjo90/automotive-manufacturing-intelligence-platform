from src.ingestion.file_tracker import calculate_file_hash


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
