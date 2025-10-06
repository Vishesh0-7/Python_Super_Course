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
    if not isinstance(a, (int, float)):
        raise TypeError(f"First argument must be int or float, got {type(a).__name__}")

    if not isinstance(b, (int, float)):
        raise TypeError(f"Second argument must be int or float, got {type(b).__name__}")

    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b
