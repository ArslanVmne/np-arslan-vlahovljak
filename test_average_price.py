import pytest

from average_price import calculate_average_price


def test_regular_case():
    assert calculate_average_price([10, 20, 30]) == 20.0


def test_single_element():
    assert calculate_average_price([49.99]) == 49.99


def test_decimal_prices():
    # (49.99 + 15.50 + 120.00) / 3 = 61.83 (zaokruženo)
    assert calculate_average_price([49.99, 15.50, 120.00]) == 61.83


def test_empty_list_raises():
    with pytest.raises(ValueError):
        calculate_average_price([])


def test_negative_price_raises():
    with pytest.raises(ValueError):
        calculate_average_price([10, -5, 30])


def test_non_numeric_price_raises():
    with pytest.raises(TypeError):
        calculate_average_price([10, "abc", 30])
