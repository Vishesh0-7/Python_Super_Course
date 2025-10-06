import pytest
import math
from solutions.ex5_design_by_contract import (
    BankAccount,
    calculate_compound_interest,
    binary_search,
    is_sorted,
    calculate_triangle_area
)


class TestBankAccount:
    """Test BankAccount class with contract validation."""

    def test_valid_account_creation(self):
        """Test valid account creation."""
        account = BankAccount(12345, 100.0)
        assert account.account_number == 12345
        assert account.get_balance() == 100.0
        assert account.transactions == []

    def test_account_creation_preconditions(self):
        """Test account creation precondition violations."""
        # Negative account number
        with pytest.raises(AssertionError, match="Account number must be positive"):
            BankAccount(-12345, 100.0)

        # Zero account number
        with pytest.raises(AssertionError, match="Account number must be positive"):
            BankAccount(0, 100.0)

        # Negative initial balance
        with pytest.raises(AssertionError, match="Initial balance must be non-negative"):
            BankAccount(12345, -100.0)

        # Invalid account number type
        with pytest.raises(AssertionError, match="Account number must be an integer"):
            BankAccount("12345", 100.0)

    def test_valid_deposits(self):
        """Test valid deposit operations."""
        account = BankAccount(12345, 100.0)

        account.deposit(50.0)
        assert account.get_balance() == 150.0
        assert len(account.transactions) == 1
        assert "Deposit: $50.00" in account.transactions[0]

        account.deposit(25.5)
        assert account.get_balance() == 175.5
        assert len(account.transactions) == 2

    def test_deposit_preconditions(self):
        """Test deposit precondition violations."""
        account = BankAccount(12345, 100.0)

        # Negative deposit
        with pytest.raises(AssertionError, match="Deposit amount must be positive"):
            account.deposit(-50.0)

        # Zero deposit
        with pytest.raises(AssertionError, match="Deposit amount must be positive"):
            account.deposit(0.0)

        # Invalid type
        with pytest.raises(AssertionError, match="Deposit amount must be numeric"):
            account.deposit("50")

    def test_valid_withdrawals(self):
        """Test valid withdrawal operations."""
        account = BankAccount(12345, 100.0)

        account.withdraw(30.0)
        assert account.get_balance() == 70.0
        assert len(account.transactions) == 1
        assert "Withdrawal: $30.00" in account.transactions[0]

        account.withdraw(70.0)  # Withdraw remaining balance
        assert account.get_balance() == 0.0

    def test_withdrawal_preconditions(self):
        """Test withdrawal precondition violations."""
        account = BankAccount(12345, 100.0)

        # Insufficient funds
        with pytest.raises(AssertionError, match="Insufficient funds"):
            account.withdraw(150.0)

        # Negative withdrawal
        with pytest.raises(AssertionError, match="Withdrawal amount must be positive"):
            account.withdraw(-30.0)

        # Zero withdrawal
        with pytest.raises(AssertionError, match="Withdrawal amount must be positive"):
            account.withdraw(0.0)

    def test_balance_invariants(self):
        """Test that balance never becomes negative."""
        account = BankAccount(12345, 50.0)

        # This should work
        account.withdraw(25.0)
        assert account.get_balance() == 25.0

        # This should fail due to insufficient funds
        with pytest.raises(AssertionError):
            account.withdraw(30.0)


class TestCompoundInterest:
    """Test compound interest calculation with contracts."""

    def test_valid_calculations(self):
        """Test valid compound interest calculations."""
        # Simple case: $1000 at 5% for 1 year, compounded annually
        result = calculate_compound_interest(1000, 0.05, 1, 1)
        assert abs(result - 1050.0) < 0.01

        # Quarterly compounding
        result = calculate_compound_interest(1000, 0.05, 1, 4)
        expected = 1000 * (1 + 0.05/4) ** (4 * 1)
        assert abs(result - expected) < 0.01

    def test_precondition_violations(self):
        """Test precondition violations."""
        # Negative principal
        with pytest.raises(AssertionError, match="Principal must be positive"):
            calculate_compound_interest(-1000, 0.05, 1, 1)

        # Negative rate
        with pytest.raises(AssertionError, match="Rate must be non-negative"):
            calculate_compound_interest(1000, -0.05, 1, 1)

        # Negative time
        with pytest.raises(AssertionError, match="Time must be non-negative"):
            calculate_compound_interest(1000, 0.05, -1, 1)

        # Zero compound frequency
        with pytest.raises(AssertionError, match="Compound frequency must be positive"):
            calculate_compound_interest(1000, 0.05, 1, 0)

    def test_zero_interest_rate(self):
        """Test zero interest rate (should return principal)."""
        result = calculate_compound_interest(1000, 0.0, 5, 1)
        assert result == 1000.0

    def test_zero_time(self):
        """Test zero time (should return principal)."""
        result = calculate_compound_interest(1000, 0.05, 0, 1)
        assert result == 1000.0


class TestBinarySearch:
    """Test binary search with contract validation."""

    def test_valid_searches(self):
        """Test valid binary search operations."""
        sorted_list = [1, 3, 5, 7, 9, 11, 13]

        # Find existing elements
        assert binary_search(sorted_list, 1) == 0
        assert binary_search(sorted_list, 7) == 3
        assert binary_search(sorted_list, 13) == 6

        # Find non-existing elements
        assert binary_search(sorted_list, 0) == -1
        assert binary_search(sorted_list, 4) == -1
        assert binary_search(sorted_list, 15) == -1

    def test_precondition_violations(self):
        """Test precondition violations."""
        # Empty list
        with pytest.raises(AssertionError, match="List cannot be empty"):
            binary_search([], 5)

        # Unsorted list
        with pytest.raises(AssertionError, match="List must be sorted"):
            binary_search([3, 1, 4, 1, 5], 3)

        # Not a list
        with pytest.raises(AssertionError, match="Input must be a list"):
            binary_search("not a list", 5)

    def test_single_element_list(self):
        """Test search in single-element list."""
        assert binary_search([5], 5) == 0
        assert binary_search([5], 3) == -1

    def test_list_unchanged_postcondition(self):
        """Test that list remains unchanged after search."""
        original = [1, 3, 5, 7, 9]
        search_list = original.copy()

        binary_search(search_list, 5)
        assert search_list == original


class TestIsSorted:
    """Test the is_sorted helper function."""

    def test_sorted_lists(self):
        """Test recognition of sorted lists."""
        assert is_sorted([])
        assert is_sorted([1])
        assert is_sorted([1, 2, 3, 4, 5])
        assert is_sorted([1, 1, 2, 2, 3])  # Equal elements allowed
        assert is_sorted([-5, -2, 0, 3, 7])

    def test_unsorted_lists(self):
        """Test recognition of unsorted lists."""
        assert not is_sorted([3, 1, 2])
        assert not is_sorted([1, 3, 2, 4])
        assert not is_sorted([5, 4, 3, 2, 1])


class TestTriangleArea:
    """Test triangle area calculation with contracts."""

    def test_valid_triangles(self):
        """Test valid triangle area calculations."""
        # Right triangle 3-4-5
        area = calculate_triangle_area(3, 4, 5)
        assert abs(area - 6.0) < 0.01

        # Equilateral triangle with side 6
        area = calculate_triangle_area(6, 6, 6)
        expected = (math.sqrt(3) / 4) * 36  # Formula for equilateral triangle
        assert abs(area - expected) < 0.01

        # Isosceles triangle
        area = calculate_triangle_area(5, 5, 8)
        assert area > 0

    def test_precondition_violations(self):
        """Test precondition violations."""
        # Negative sides
        with pytest.raises(AssertionError, match="Side a must be positive"):
            calculate_triangle_area(-3, 4, 5)

        with pytest.raises(AssertionError, match="Side b must be positive"):
            calculate_triangle_area(3, -4, 5)

        with pytest.raises(AssertionError, match="Side c must be positive"):
            calculate_triangle_area(3, 4, -5)

        # Zero sides
        with pytest.raises(AssertionError, match="Side a must be positive"):
            calculate_triangle_area(0, 4, 5)

        # Triangle inequality violations
        with pytest.raises(AssertionError, match="Triangle inequality violated"):
            calculate_triangle_area(1, 1, 5)  # 1 + 1 <= 5

        with pytest.raises(AssertionError, match="Triangle inequality violated"):
            calculate_triangle_area(1, 5, 1)  # 1 + 1 <= 5

        with pytest.raises(AssertionError, match="Triangle inequality violated"):
            calculate_triangle_area(5, 1, 1)  # 1 + 1 <= 5

    def test_edge_cases(self):
        """Test edge cases for triangle calculation."""
        # Very small triangle
        area = calculate_triangle_area(0.1, 0.1, 0.1)
        assert area > 0

        # Large triangle
        area = calculate_triangle_area(100, 100, 100)
        assert area > 0

    def test_type_validation(self):
        """Test type validation for triangle sides."""
        with pytest.raises(AssertionError, match="Side a must be numeric"):
            calculate_triangle_area("3", 4, 5)

        with pytest.raises(AssertionError, match="Side b must be numeric"):
            calculate_triangle_area(3, "4", 5)

        with pytest.raises(AssertionError, match="Side c must be numeric"):
            calculate_triangle_area(3, 4, "5")
