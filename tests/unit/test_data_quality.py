from src.common.data_quality import should_create_invalid_record

def test_probability_zero_never_invalid():
    result = should_create_invalid_record(0)
    assert result is False


def test_probability_one_always_invalid():
    result = should_create_invalid_record(1)
    assert result is True