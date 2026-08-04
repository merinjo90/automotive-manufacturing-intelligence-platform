from datetime import date
from src.common.date_helpers import genetare_random_date

def test_zero_offset_returns_start_date():
    result = genetare_random_date(date(2026, 1, 1), 0)
    assert result == date(2026, 1, 1)

def test_max_offset_returns_latest_date():
    result = genetare_random_date(date(2026, 1, 1),10)
    assert result <= date(2026, 1, 11)
    assert result >= date(2026, 1, 1)