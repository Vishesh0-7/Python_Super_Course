# A1 - Defensive Programming

**Duration:** 3-4 hours
**Prerequisites:** Testing foundations, Python basics
**Difficulty:** Intermediate

## Learning Objectives

By the end of this module, you will be able to:

- Apply EAFP (Easier to Ask for Forgiveness than Permission) vs LBYL (Look Before You Leap) patterns appropriately
- Implement robust input validation and type checking
- Design and use custom exceptions for clearer error communication
- Write guard clauses to simplify complex conditional logic
- Apply design by contract principles with pre/post-conditions
- Create resilient code that fails fast with actionable error messages
- Write comprehensive tests for error scenarios and edge cases

## Key Defensive Programming Principles

### 1. Fail Fast and Clear
When something goes wrong, detect it immediately and provide actionable error messages.

```python
def process_user_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be an integer, got {type(age).__name__}")
    if age < 0:
        raise ValueError(f"Age cannot be negative, got {age}")
    if age > 150:
        raise ValueError(f"Age seems unrealistic, got {age}")
    return f"Processing age: {age}"
```

### 2. EAFP vs LBYL

**EAFP (Easier to Ask for Forgiveness than Permission):**
```python
# Good for file operations, dictionary access
try:
    return data['key']
except KeyError:
    return None
```

**LBYL (Look Before You Leap):**
```python
# Good for type checking, mathematical constraints
if isinstance(x, (int, float)) and x >= 0:
    return math.sqrt(x)
else:
    raise ValueError("Input must be a non-negative number")
```

### 3. Guard Clauses
Simplify complex conditionals by handling edge cases early:

```python
def calculate_discount(price, customer_type, loyalty_years):
    # Guard clauses
    if price <= 0:
        raise ValueError("Price must be positive")
    if customer_type not in ['regular', 'premium', 'vip']:
        raise ValueError(f"Invalid customer type: {customer_type}")
    if loyalty_years < 0:
        raise ValueError("Loyalty years cannot be negative")

    # Main logic becomes clearer
    base_discount = 0.1 if customer_type == 'premium' else 0.2 if customer_type == 'vip' else 0
    loyalty_bonus = min(loyalty_years * 0.01, 0.1)
    return price * (1 - base_discount - loyalty_bonus)
```

### 4. Custom Exceptions
Create domain-specific exceptions for better error handling:

```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class BusinessRuleError(Exception):
    """Raised when business logic constraints are violated."""
    pass
```

## Exercises

Complete the following exercises to master defensive programming concepts:

### Exercise 1: Input Validation (`ex1_validate_input.py`)
Practice basic type checking and value validation with a safe division function.

### Exercise 2: Guard Clauses (`ex2_guard_clauses.py`)
Refactor nested conditionals using guard clauses to improve readability.

### Exercise 3: Custom Exceptions (`ex3_custom_exceptions.py`)
Design domain-specific exceptions for a user registration system.

### Exercise 4: EAFP vs LBYL (`ex4_eafp_vs_lbyl.py`)
Implement both patterns appropriately for different scenarios.

### Exercise 5: Design by Contract (`ex5_design_by_contract.py`)
Apply pre/post-conditions to ensure function contracts are maintained.

### Exercise 6: Error Recovery (`ex6_error_recovery.py`)
Implement graceful error recovery with logging and fallback mechanisms.

## How to Work with This Module

1. **Read each exercise** in the `exercises/` directory
2. **Implement your solution** based on the problem statement and hints
3. **Check your work** by comparing with `solutions/` (only after attempting!)
4. **Run the tests** to verify correctness:
   ```bash
   # ✅ RECOMMENDED: Run specific exercise tests (clean output)
   python -m pytest tests/test_ex1_validate_input.py -v --no-cov

   # ✅ ALTERNATIVE: Run with coverage on your solutions
   python -m pytest tests/test_ex1_validate_input.py -v --cov=solutions --cov-fail-under=0

   # ✅ QUICK SCRIPT: Use the provided helper script
   ./check_exercise.sh 1    # Check exercise 1
   ./check_exercise.sh      # Check all exercises

   # Run all tests at once
   python -m pytest tests/ -v --no-cov
   ```## Verification

All solutions must:
- ✅ Pass their respective test suites
- ✅ Handle edge cases gracefully
- ✅ Use appropriate error types
- ✅ Include meaningful error messages
- ✅ Follow Python coding standards

## Quick Tips

- **Start simple**: Begin with basic validation, then add complexity
- **Test error paths**: Don't just test the happy path
- **Be specific**: Generic exceptions are rarely helpful
- **Document contracts**: Make function expectations clear
- **Log thoughtfully**: Include context without exposing sensitive data

## Common Pitfalls to Avoid

- Using bare `except:` clauses
- Overusing exceptions for control flow
- Returning `None` or magic values instead of raising exceptions
- Leaking sensitive information in error messages
- Writing overly generic error messages

Ready to write more resilient code? Start with Exercise 1!
