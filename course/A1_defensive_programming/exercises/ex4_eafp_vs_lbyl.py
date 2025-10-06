"""
Exercise 4: EAFP vs LBYL - Choosing the Right Approach

Implement functions using both EAFP (Easier to Ask for Forgiveness than Permission)
and LBYL (Look Before You Leap) patterns where each is most appropriate.

Learn when to use each approach:
- EAFP: When exceptions are the natural way to handle the case (file I/O, dict access, etc.)
- LBYL: When checking conditions is cheaper and clearer (type/value validation)

Requirements:
- Implement both approaches appropriately for different scenarios
- Understand the trade-offs between each approach
- Write code that's both efficient and readable
"""

import json
import os
from typing import Any, Dict, Optional

# Hint: EAFP is good for operations that might fail naturally (I/O, parsing, etc.)
# Hint: LBYL is good for type/value checks that should be done upfront
# Hint: Consider performance implications and readability
# Hint: Think about what exceptions are "expected" vs truly exceptional

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
    # TODO: Implement using EAFP approach
    # Try to access the nested keys, catch KeyError if any key is missing
    pass


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
    # TODO: Implement using LBYL approach
    # Check type first, then check range, then return
    pass


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
    # TODO: Implement using EAFP approach
    # Try to open and parse the file, let natural exceptions bubble up
    pass


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
    # TODO: Implement hybrid approach
    # Use LBYL for type and value validation
    # Use EAFP for the mathematical operation (though division by zero is checked)
    pass


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
    # TODO: Implement using EAFP approach
    # Try to access the preference, return default if not found
    pass


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
    # TODO: Implement using EAFP approach
    # Try to convert each item, let ValueError bubble up if conversion fails
    pass


if __name__ == "__main__":
    # Quick manual tests

    # Test nested value access
    test_data = {
        "user": {
            "profile": {"name": "Alice", "age": 30},
            "settings": {"theme": "dark"}
        }
    }

    print("=== Testing nested value access (EAFP) ===")
    print(f"user.profile.name: {safe_get_nested_value(test_data, 'user.profile.name')}")
    print(f"user.missing.key: {safe_get_nested_value(test_data, 'user.missing.key')}")

    print("\n=== Testing numeric validation (LBYL) ===")
    try:
        result = validate_numeric_range(25.5, 0, 100)
        print(f"Valid number: {result}")

        result = validate_numeric_range("not a number", 0, 100)
        print(f"Should not reach here: {result}")
    except (TypeError, ValueError) as e:
        print(f"Caught expected error: {e}")

    print("\n=== Testing BMI calculation (Hybrid) ===")
    try:
        bmi = calculate_bmi(70, 1.75)
        print(f"BMI: {bmi:.2f}")

        bmi = calculate_bmi("70", 1.75)  # Should raise TypeError
        print(f"Should not reach here: {bmi}")
    except (TypeError, ValueError) as e:
        print(f"Caught expected error: {e}")

    print("\n=== Testing integer list parsing (EAFP) ===")
    try:
        numbers = parse_integer_list("1,2,3,4,5")
        print(f"Parsed numbers: {numbers}")

        numbers = parse_integer_list("1,2,abc,4")  # Should raise ValueError
        print(f"Should not reach here: {numbers}")
    except ValueError as e:
        print(f"Caught expected error: {e}")
