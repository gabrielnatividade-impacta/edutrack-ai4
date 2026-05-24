import pytest
from scripts.calculate_progress import calculate_progress, progress_json


def test_calculate_progress_basic():
    result = calculate_progress(30, 50)
    assert result["completed"] == 30
    assert result["total"] == 50
    assert result["progress_percent"] == 60.0


def test_calculate_progress_clamps_at_100():
    result = calculate_progress(120, 100)
    assert result["progress_percent"] == 100.0


def test_calculate_progress_negative_values():
    with pytest.raises(ValueError):
        calculate_progress(-1, 10)

    with pytest.raises(ValueError):
        calculate_progress(1, -10)


def test_calculate_progress_zero_total():
    with pytest.raises(ValueError):
        calculate_progress(10, 0)


def test_progress_json_output():
    output = progress_json(25, 50)
    assert "\"progress_percent\": 50.0" in output
