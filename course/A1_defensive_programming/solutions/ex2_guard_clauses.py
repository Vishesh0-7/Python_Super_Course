def calculate_shipping_cost(weight, distance, shipping_type, is_express):
    """
    Calculate shipping cost based on multiple factors.

    Args:
        weight (float): Package weight in kg (must be > 0, <= 50)
        distance (float): Shipping distance in km (must be > 0)
        shipping_type (str): 'standard', 'priority', or 'overnight'
        is_express (bool): Whether express handling is requested

    Returns:
        float: Total shipping cost

    Raises:
        ValueError: For invalid input values
        TypeError: For invalid input types

    Business Rules:
    - Weight must be positive and not exceed 50kg
    - Distance must be positive
    - Shipping type must be one of the valid options
    - Base cost = weight * 2.5 + distance * 0.1
    - Priority adds 25%, overnight adds 50%
    - Express handling adds $10 flat fee
    """
    # Guard clause: Check types first
    if not isinstance(weight, (int, float)):
        raise TypeError("Weight must be numeric (int or float)")

    if not isinstance(distance, (int, float)):
        raise TypeError("Distance must be numeric (int or float)")

    if not isinstance(shipping_type, str):
        raise TypeError("Shipping type must be a string")

    if not isinstance(is_express, bool):
        raise TypeError("is_express must be a boolean")

    # Guard clause: Check weight constraints
    if weight <= 0:
        raise ValueError("Weight must be positive")

    if weight > 50:
        raise ValueError("Weight cannot exceed 50kg")

    # Guard clause: Check distance constraints
    if distance <= 0:
        raise ValueError("Distance must be positive")

    # Guard clause: Check valid shipping types
    valid_types = ['standard', 'priority', 'overnight']
    if shipping_type not in valid_types:
        raise ValueError(f"Invalid shipping type '{shipping_type}'. Must be one of: {valid_types}")

    # Main calculation logic (clean and focused)
    base_cost = weight * 2.5 + distance * 0.1

    # Apply shipping type multiplier
    if shipping_type == 'priority':
        base_cost *= 1.25
    elif shipping_type == 'overnight':
        base_cost *= 1.5

    # Add express handling fee
    if is_express:
        base_cost += 10

    return base_cost
