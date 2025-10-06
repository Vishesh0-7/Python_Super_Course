import json
import os
from typing import Any, Dict, Optional


def safe_get_nested_value(data: Dict[str, Any], key_path: str) -> Optional[Any]:
    """
    Get a nested value from a dictionary using dot notation.
    Use EAFP approach since dictionary access naturally raises KeyError.

    Args:
        data: Dictionary to search in
        key_path: Dot-separated path like "user.profile.name"

    Returns:
        The value if found, None if any key in the path doesn't exist

    Example:
        data = {"user": {"profile": {"name": "John"}}}
        safe_get_nested_value(data, "user.profile.name") -> "John"
        safe_get_nested_value(data, "user.missing.field") -> None
    """
    try:
        keys = key_path.split('.')
        current = data
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return None


def validate_numeric_range(value: Any, min_val: float, max_val: float) -> float:
    """
    Validate that a value is numeric and within a specified range.
    Use LBYL approach since type/value checking is straightforward.

    Args:
        value: Value to validate
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        The value as a float if valid

    Raises:
        TypeError: If value is not numeric
        ValueError: If value is outside the allowed range
    """
    # LBYL: Check type first
    if not isinstance(value, (int, float)):
        raise TypeError(f"Value must be numeric, got {type(value).__name__}")

    # LBYL: Check range
    if value < min_val:
        raise ValueError(f"Value {value} is below minimum {min_val}")

    if value > max_val:
        raise ValueError(f"Value {value} is above maximum {max_val}")

    return float(value)


def load_config_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON configuration file.
    Use EAFP approach since file operations naturally raise exceptions.

    Args:
        file_path: Path to the JSON config file

    Returns:
        Parsed configuration as a dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
        PermissionError: If file can't be read
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in configuration file: {e.msg}", e.doc, e.pos)
    except PermissionError:
        raise PermissionError(f"Permission denied reading configuration file: {file_path}")


def calculate_bmi(weight: Any, height: Any) -> float:
    """
    Calculate BMI (Body Mass Index) with input validation.
    Use LBYL for input validation, EAFP for calculation.

    Args:
        weight: Weight in kg
        height: Height in meters

    Returns:
        BMI value

    Raises:
        TypeError: If inputs are not numeric
        ValueError: If inputs are not positive or height is zero
    """
    # LBYL: Type validation
    if not isinstance(weight, (int, float)):
        raise TypeError(f"Weight must be numeric, got {type(weight).__name__}")

    if not isinstance(height, (int, float)):
        raise TypeError(f"Height must be numeric, got {type(height).__name__}")

    # LBYL: Value validation
    if weight <= 0:
        raise ValueError("Weight must be positive")

    if height <= 0:
        raise ValueError("Height must be positive")

    # EAFP: Perform calculation (though we've already checked for zero)
    try:
        return weight / (height * height)
    except ZeroDivisionError:
        # This shouldn't happen due to our checks, but defensive programming
        raise ValueError("Height cannot be zero")


def get_user_preference(user_data: Dict[str, Any], preference_key: str, default: Any = None) -> Any:
    """
    Get a user preference with fallback to default.
    Use EAFP approach for dictionary access.

    Args:
        user_data: User's data dictionary
        preference_key: Key for the preference to retrieve
        default: Default value if preference not found

    Returns:
        User's preference value or default
    """
    try:
        return user_data['preferences'][preference_key]
    except (KeyError, TypeError):
        return default


def parse_integer_list(input_string: str) -> list[int]:
    """
    Parse a comma-separated string into a list of integers.
    Use EAFP approach since parsing naturally raises exceptions.

    Args:
        input_string: String like "1,2,3,4"

    Returns:
        List of integers

    Raises:
        ValueError: If any item cannot be converted to integer
    """
    if not input_string.strip():
        return []

    try:
        return [int(item.strip()) for item in input_string.split(',')]
    except ValueError as e:
        raise ValueError(f"Invalid integer in input string: {e}")
