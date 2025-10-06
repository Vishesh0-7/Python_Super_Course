import pytest
from solutions.ex1_validate_input import safe_divide
#from exercises.ex1_validate_input import safe_divide

def test_valid_division():
    """Test normal division operations."""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(15, 3) == 5.0
    assert safe_divide(7, 2) == 3.5
    assert safe_divide(5.5, 1.1) == 5.0


def test_negative_numbers():
    """Test division with negative numbers."""
    assert safe_divide(-10, 2) == -5.0
    assert safe_divide(10, -2) == -5.0
    assert safe_divide(-10, -2) == 5.0


def test_zero_division():
    """Test that division by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        safe_divide(5, 0)

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        safe_divide(10.5, 0.0)


def test_type_errors():
    """Test that invalid types raise TypeError."""
    # String inputs
    with pytest.raises(TypeError, match="First argument must be int or float, got str"):
        safe_divide("5", 2)

    with pytest.raises(TypeError, match="Second argument must be int or float, got str"):
        safe_divide(5, "2")

    # None inputs
    with pytest.raises(TypeError):
        safe_divide(None, 2)

    with pytest.raises(TypeError):
        safe_divide(5, None)

    # List inputs
    with pytest.raises(TypeError):
        safe_divide([5], 2)

    with pytest.raises(TypeError):
        safe_divide(5, [2])


def test_edge_cases():
    """Test edge cases and special values."""
    # Very small numbers
    assert safe_divide(0.1, 0.1) == 1.0

    # Large numbers
    assert safe_divide(1000000, 1000) == 1000.0

    # Division resulting in zero
    assert safe_divide(0, 5) == 0.0
    assert safe_divide(0.0, 10) == 0.0


def test_return_type():
    """Test that function always returns float."""
    result = safe_divide(10, 2)
    assert isinstance(result, float)

    result = safe_divide(5, 2)
    assert isinstance(result, float)
