"""
Exercise 5: Design by Contract - Pre/Post Conditions

Implement functions with explicit contracts using assertions and validation.

Design by Contract principles:
- Preconditions: What must be true when the function is called
- Postconditions: What must be true when the function returns
- Invariants: What must always be true for the object/data

Requirements:
- Use assertions to check preconditions and postconditions
- Implement clear contract violations with helpful messages
- Balance between defensive programming and performance
- Document contracts clearly
"""

import math
from typing import List

# Hint: Use assert statements for conditions that should never fail in correct usage
# Hint: Use exceptions for conditions that might fail due to user input
# Hint: Consider when to use assertions vs explicit validation
# Hint: Think about what contracts help prevent bugs

class BankAccount:
    """
    A bank account with defensive contract checks.

    Invariants:
    - Balance must never be negative (for this simple account type)
    - Account number must be positive
    - Transaction history must be chronologically ordered
    """

    def __init__(self, account_number: int, initial_balance: float = 0.0):
        """
        Initialize a bank account.

        Preconditions:
        - account_number must be positive
        - initial_balance must be non-negative
        """
        # TODO: Add precondition checks
        # TODO: Initialize instance variables
        # TODO: Add postcondition checks
        pass

    def deposit(self, amount: float) -> None:
        """
        Deposit money into the account.

        Preconditions:
        - amount must be positive
        - account must be in valid state

        Postconditions:
        - balance increases by amount
        - transaction is recorded
        """
        # TODO: Add precondition checks
        # TODO: Implement deposit logic
        # TODO: Add postcondition checks
        pass

    def withdraw(self, amount: float) -> None:
        """
        Withdraw money from the account.

        Preconditions:
        - amount must be positive
        - sufficient balance must be available
        - account must be in valid state

        Postconditions:
        - balance decreases by amount
        - transaction is recorded
        - balance remains non-negative
        """
        # TODO: Add precondition checks
        # TODO: Implement withdrawal logic
        # TODO: Add postcondition checks
        pass

    def get_balance(self) -> float:
        """Get current balance with invariant checking."""
        # TODO: Check invariants before returning
        pass

    def _check_invariants(self) -> None:
        """Check class invariants - call this in public methods."""
        # TODO: Implement invariant checks
        pass


def calculate_compound_interest(principal: float, rate: float, time: int,
                              compound_frequency: int = 1) -> float:
    """
    Calculate compound interest with contract validation.

    Preconditions:
    - principal must be positive
    - rate must be non-negative (allow 0% interest)
    - time must be non-negative
    - compound_frequency must be positive

    Postconditions:
    - result must be >= principal (assuming non-negative rate)
    - result must be finite and positive

    Formula: A = P(1 + r/n)^(nt)
    """
    # TODO: Add precondition checks with assertions

    # TODO: Implement calculation

    # TODO: Add postcondition checks

    pass


def binary_search(sorted_list: List[int], target: int) -> int:
    """
    Perform binary search with contract validation.

    Preconditions:
    - sorted_list must be sorted in ascending order
    - sorted_list must not be empty

    Postconditions:
    - if target found: result is valid index where sorted_list[result] == target
    - if target not found: result is -1
    - sorted_list remains unchanged

    Returns:
        Index of target if found, -1 otherwise
    """
    # TODO: Add precondition checks
    # How do you efficiently check if a list is sorted?

    # TODO: Store original list for postcondition checking

    # TODO: Implement binary search

    # TODO: Add postcondition checks

    pass


def is_sorted(lst: List[int]) -> bool:
    """Helper function to check if a list is sorted."""
    # TODO: Implement efficient sorted check
    pass


def calculate_triangle_area(side_a: float, side_b: float, side_c: float) -> float:
    """
    Calculate triangle area using Heron's formula with contract validation.

    Preconditions:
    - All sides must be positive
    - Sides must form a valid triangle (triangle inequality)

    Postconditions:
    - Area must be positive
    - Area must be finite

    Triangle inequality: sum of any two sides > third side
    """
    # TODO: Add precondition checks
    # Check triangle inequality: a + b > c, a + c > b, b + c > a

    # TODO: Calculate area using Heron's formula
    # s = (a + b + c) / 2
    # area = sqrt(s * (s-a) * (s-b) * (s-c))

    # TODO: Add postcondition checks

    pass


if __name__ == "__main__":
    print("=== Testing BankAccount ===")
    try:
        # Valid operations
        account = BankAccount(12345, 100.0)
        print(f"Initial balance: ${account.get_balance():.2f}")

        account.deposit(50.0)
        print(f"After deposit: ${account.get_balance():.2f}")

        account.withdraw(30.0)
        print(f"After withdrawal: ${account.get_balance():.2f}")

        # Invalid operations
        account.withdraw(200.0)  # Should fail - insufficient funds

    except (AssertionError, ValueError) as e:
        print(f"Caught expected error: {e}")

    print("\n=== Testing Compound Interest ===")
    try:
        result = calculate_compound_interest(1000, 0.05, 10, 4)
        print(f"Compound interest result: ${result:.2f}")

        # Invalid input
        result = calculate_compound_interest(-1000, 0.05, 10, 4)  # Negative principal
    except AssertionError as e:
        print(f"Caught contract violation: {e}")

    print("\n=== Testing Binary Search ===")
    try:
        sorted_nums = [1, 3, 5, 7, 9, 11, 13]
        index = binary_search(sorted_nums, 7)
        print(f"Found 7 at index: {index}")

        index = binary_search(sorted_nums, 8)
        print(f"8 not found, returned: {index}")

        # Invalid input
        index = binary_search([3, 1, 2], 2)  # Unsorted list
    except AssertionError as e:
        print(f"Caught contract violation: {e}")

    print("\n=== Testing Triangle Area ===")
    try:
        area = calculate_triangle_area(3, 4, 5)  # Valid right triangle
        print(f"Triangle area: {area:.2f}")

        # Invalid triangle
        area = calculate_triangle_area(1, 1, 5)  # Violates triangle inequality
    except (AssertionError, ValueError) as e:
        print(f"Caught contract violation: {e}")
