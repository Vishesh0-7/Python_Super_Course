"""
Exercise 1: Input Validation and Type Checking

Write a function `safe_divide(a, b)` that performs division with proper input validation.

Requirements:
- If either input is not a number (int or float), raise TypeError with a descriptive message
- If b is zero, raise ValueError with a descriptive message
- Return the result of a / b for valid inputs

Your function should handle edge cases gracefully and provide clear error messages
that help users understand what went wrong.

Test your understanding:
- What's the difference between TypeError and ValueError?
- When should you check types vs values?
- How can error messages be more helpful?
"""

# Hint: Use isinstance() to check if inputs are numeric types
# Hint: Check for zero division before performing the operation
# Hint: Include the actual values in error messages to help debugging
# Hint: Consider what types should be accepted - int, float, or others?

def safe_divide(a, b):
    """
    Safely divide two numbers with input validation.

    Args:
        a: Numerator (must be int or float)
        b: Denominator (must be int or float, cannot be zero)

    Returns:
        float: Result of a / b

    Raises:
        TypeError: If inputs are not numeric
        ValueError: If b is zero
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    # Quick manual tests - try running this file!
    try:
        print(f"10 / 2 = {safe_divide(10, 2)}")
        print(f"5.5 / 1.1 = {safe_divide(5.5, 1.1)}")

        # These should raise exceptions:
        print(safe_divide("10", 2))  # Should raise TypeError
    except Exception as e:
        print(f"Caught expected error: {e}")

    try:
        print(safe_divide(10, 0))  # Should raise ValueError
    except Exception as e:
        print(f"Caught expected error: {e}")
