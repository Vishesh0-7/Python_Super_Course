import math
from typing import List


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
        # Precondition checks
        assert isinstance(account_number, int), "Account number must be an integer"
        assert account_number > 0, f"Account number must be positive, got {account_number}"
        assert isinstance(initial_balance, (int, float)), "Initial balance must be numeric"
        assert initial_balance >= 0, f"Initial balance must be non-negative, got {initial_balance}"

        self.account_number = account_number
        self.balance = float(initial_balance)
        self.transactions = []

        # Postcondition checks
        self._check_invariants()

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
        # Precondition checks
        assert isinstance(amount, (int, float)), "Deposit amount must be numeric"
        assert amount > 0, f"Deposit amount must be positive, got {amount}"
        self._check_invariants()

        old_balance = self.balance

        # Perform operation
        self.balance += amount
        self.transactions.append(f"Deposit: ${amount:.2f}")

        # Postcondition checks
        assert self.balance == old_balance + amount, "Balance not updated correctly"
        assert len(self.transactions) > 0, "Transaction not recorded"
        self._check_invariants()

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
        # Precondition checks
        assert isinstance(amount, (int, float)), "Withdrawal amount must be numeric"
        assert amount > 0, f"Withdrawal amount must be positive, got {amount}"
        assert self.balance >= amount, f"Insufficient funds: balance {self.balance}, requested {amount}"
        self._check_invariants()

        old_balance = self.balance

        # Perform operation
        self.balance -= amount
        self.transactions.append(f"Withdrawal: ${amount:.2f}")

        # Postcondition checks
        assert self.balance == old_balance - amount, "Balance not updated correctly"
        assert self.balance >= 0, "Balance became negative"
        assert len(self.transactions) > 0, "Transaction not recorded"
        self._check_invariants()

    def get_balance(self) -> float:
        """Get current balance with invariant checking."""
        self._check_invariants()
        return self.balance

    def _check_invariants(self) -> None:
        """Check class invariants - call this in public methods."""
        assert hasattr(self, 'account_number'), "Account number not set"
        assert self.account_number > 0, "Account number must be positive"
        assert hasattr(self, 'balance'), "Balance not set"
        assert self.balance >= 0, f"Balance cannot be negative, got {self.balance}"
        assert hasattr(self, 'transactions'), "Transaction history not set"


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
    # Precondition checks
    assert isinstance(principal, (int, float)), "Principal must be numeric"
    assert principal > 0, f"Principal must be positive, got {principal}"
    assert isinstance(rate, (int, float)), "Rate must be numeric"
    assert rate >= 0, f"Rate must be non-negative, got {rate}"
    assert isinstance(time, int), "Time must be an integer"
    assert time >= 0, f"Time must be non-negative, got {time}"
    assert isinstance(compound_frequency, int), "Compound frequency must be an integer"
    assert compound_frequency > 0, f"Compound frequency must be positive, got {compound_frequency}"

    # Calculate compound interest
    result = principal * (1 + rate / compound_frequency) ** (compound_frequency * time)

    # Postcondition checks
    assert result >= principal, f"Result {result} should be >= principal {principal}"
    assert math.isfinite(result), "Result must be finite"
    assert result > 0, "Result must be positive"

    return result


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
    # Precondition checks
    assert isinstance(sorted_list, list), "Input must be a list"
    assert len(sorted_list) > 0, "List cannot be empty"
    assert is_sorted(sorted_list), "List must be sorted in ascending order"

    # Store original for postcondition checking
    original_list = sorted_list.copy()

    # Perform binary search
    left, right = 0, len(sorted_list) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            # Postcondition checks for found case
            assert 0 <= mid < len(sorted_list), "Result index out of bounds"
            assert sorted_list[mid] == target, "Result index doesn't contain target"
            assert sorted_list == original_list, "List was modified during search"
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # Postcondition checks for not found case
    assert sorted_list == original_list, "List was modified during search"
    return -1


def is_sorted(lst: List[int]) -> bool:
    """Helper function to check if a list is sorted."""
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


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
    # Precondition checks
    assert isinstance(side_a, (int, float)), "Side a must be numeric"
    assert isinstance(side_b, (int, float)), "Side b must be numeric"
    assert isinstance(side_c, (int, float)), "Side c must be numeric"
    assert side_a > 0, f"Side a must be positive, got {side_a}"
    assert side_b > 0, f"Side b must be positive, got {side_b}"
    assert side_c > 0, f"Side c must be positive, got {side_c}"

    # Check triangle inequality
    assert side_a + side_b > side_c, f"Triangle inequality violated: {side_a} + {side_b} <= {side_c}"
    assert side_a + side_c > side_b, f"Triangle inequality violated: {side_a} + {side_c} <= {side_b}"
    assert side_b + side_c > side_a, f"Triangle inequality violated: {side_b} + {side_c} <= {side_a}"

    # Calculate area using Heron's formula
    s = (side_a + side_b + side_c) / 2
    area = math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

    # Postcondition checks
    assert area > 0, f"Area must be positive, got {area}"
    assert math.isfinite(area), "Area must be finite"

    return area
