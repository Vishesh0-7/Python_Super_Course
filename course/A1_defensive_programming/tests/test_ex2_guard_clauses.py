import pytest
from solutions.ex2_guard_clauses import calculate_shipping_cost


def test_valid_shipping_calculations():
    """Test valid shipping cost calculations."""
    # Standard shipping
    cost = calculate_shipping_cost(5, 100, 'standard', False)
    expected = 5 * 2.5 + 100 * 0.1  # 12.5 + 10 = 22.5
    assert cost == expected

    # Priority shipping (25% increase)
    cost = calculate_shipping_cost(5, 100, 'priority', False)
    expected = (5 * 2.5 + 100 * 0.1) * 1.25  # 22.5 * 1.25 = 28.125
    assert cost == expected

    # Overnight shipping (50% increase)
    cost = calculate_shipping_cost(5, 100, 'overnight', False)
    expected = (5 * 2.5 + 100 * 0.1) * 1.5  # 22.5 * 1.5 = 33.75
    assert cost == expected


def test_express_handling():
    """Test express handling fee."""
    # Standard with express
    cost = calculate_shipping_cost(5, 100, 'standard', True)
    expected = 5 * 2.5 + 100 * 0.1 + 10  # 22.5 + 10 = 32.5
    assert cost == expected

    # Priority with express
    cost = calculate_shipping_cost(5, 100, 'priority', True)
    expected = (5 * 2.5 + 100 * 0.1) * 1.25 + 10  # 28.125 + 10 = 38.125
    assert cost == expected


def test_type_errors():
    """Test that invalid types raise TypeError."""
    # Invalid weight type
    with pytest.raises(TypeError, match="Weight must be numeric"):
        calculate_shipping_cost("5", 100, 'standard', False)

    # Invalid distance type
    with pytest.raises(TypeError, match="Distance must be numeric"):
        calculate_shipping_cost(5, "100", 'standard', False)

    # Invalid shipping type
    with pytest.raises(TypeError, match="Shipping type must be a string"):
        calculate_shipping_cost(5, 100, 123, False)

    # Invalid express flag
    with pytest.raises(TypeError, match="is_express must be a boolean"):
        calculate_shipping_cost(5, 100, 'standard', "yes")


def test_weight_validation():
    """Test weight validation rules."""
    # Negative weight
    with pytest.raises(ValueError, match="Weight must be positive"):
        calculate_shipping_cost(-5, 100, 'standard', False)

    # Zero weight
    with pytest.raises(ValueError, match="Weight must be positive"):
        calculate_shipping_cost(0, 100, 'standard', False)

    # Weight too high
    with pytest.raises(ValueError, match="Weight cannot exceed 50kg"):
        calculate_shipping_cost(51, 100, 'standard', False)

    # Maximum valid weight
    cost = calculate_shipping_cost(50, 100, 'standard', False)
    assert cost > 0


def test_distance_validation():
    """Test distance validation rules."""
    # Negative distance
    with pytest.raises(ValueError, match="Distance must be positive"):
        calculate_shipping_cost(5, -100, 'standard', False)

    # Zero distance
    with pytest.raises(ValueError, match="Distance must be positive"):
        calculate_shipping_cost(5, 0, 'standard', False)


def test_shipping_type_validation():
    """Test shipping type validation."""
    # Invalid shipping type
    with pytest.raises(ValueError, match="Invalid shipping type 'express'"):
        calculate_shipping_cost(5, 100, 'express', False)

    with pytest.raises(ValueError, match="Invalid shipping type 'fast'"):
        calculate_shipping_cost(5, 100, 'fast', False)

    # Case sensitivity
    with pytest.raises(ValueError, match="Invalid shipping type 'Standard'"):
        calculate_shipping_cost(5, 100, 'Standard', False)


def test_edge_cases():
    """Test edge cases."""
    # Minimum valid values
    cost = calculate_shipping_cost(0.1, 0.1, 'standard', False)
    assert cost > 0

    # Float values
    cost = calculate_shipping_cost(5.5, 100.5, 'priority', True)
    assert cost > 0

    # Maximum weight with overnight express
    cost = calculate_shipping_cost(50, 1000, 'overnight', True)
    expected = (50 * 2.5 + 1000 * 0.1) * 1.5 + 10  # (125 + 100) * 1.5 + 10 = 347.5
    assert cost == expected


def test_all_shipping_types():
    """Test all valid shipping types work."""
    valid_types = ['standard', 'priority', 'overnight']

    for shipping_type in valid_types:
        cost = calculate_shipping_cost(10, 50, shipping_type, False)
        assert cost > 0
