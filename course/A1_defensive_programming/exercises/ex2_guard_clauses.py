"""
Exercise 2: Guard Clauses for Cleaner Logic

Refactor a nested conditional function using guard clauses to improve readability.

You're given a function that calculates shipping cost with many nested conditions.
Your task is to refactor it using guard clauses to make it more readable and maintainable.

Requirements:
- Use guard clauses to handle invalid inputs early
- Raise appropriate exceptions for invalid conditions
- Keep the same business logic but improve the structure
- Ensure all edge cases are handled

Guard clauses help you:
- Reduce nesting levels
- Make the happy path more obvious
- Handle edge cases explicitly
- Improve code readability
"""

# Hint: Handle invalid cases first with early returns/raises
# Hint: Each guard clause should check one specific condition
# Hint: Use descriptive error messages that explain the business rules
# Hint: The main logic should be at the end, after all validations

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

    # TODO: Add guard clauses here to validate inputs
    # Check types first, then values, then business rules

    # TODO: Implement the main calculation logic here
    # This should be clean and focused on the happy path

    pass


# Original nested version for reference (don't modify):
def calculate_shipping_cost_nested(weight, distance, shipping_type, is_express):
    """Original version with nested conditions - for comparison only."""
    if isinstance(weight, (int, float)) and isinstance(distance, (int, float)):
        if isinstance(shipping_type, str) and isinstance(is_express, bool):
            if weight > 0 and weight <= 50:
                if distance > 0:
                    if shipping_type in ['standard', 'priority', 'overnight']:
                        base_cost = weight * 2.5 + distance * 0.1
                        if shipping_type == 'priority':
                            base_cost *= 1.25
                        elif shipping_type == 'overnight':
                            base_cost *= 1.5
                        if is_express:
                            base_cost += 10
                        return base_cost
                    else:
                        raise ValueError(f"Invalid shipping type: {shipping_type}")
                else:
                    raise ValueError("Distance must be positive")
            else:
                raise ValueError("Weight must be positive and not exceed 50kg")
        else:
            raise TypeError("Invalid input types")
    else:
        raise TypeError("Weight and distance must be numeric")


if __name__ == "__main__":
    # Quick manual tests
    try:
        print(f"Standard 5kg, 100km: ${calculate_shipping_cost(5, 100, 'standard', False):.2f}")
        print(f"Express overnight 2kg, 50km: ${calculate_shipping_cost(2, 50, 'overnight', True):.2f}")

        # Test error cases:
        print(calculate_shipping_cost(-5, 100, 'standard', False))  # Should raise ValueError
    except Exception as e:
        print(f"Caught expected error: {e}")
