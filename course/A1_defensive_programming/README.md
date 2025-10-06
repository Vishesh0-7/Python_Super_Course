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
   ```

## Extended Concepts & Deep Dive

### Why Defensive Programming?
Defensive programming reduces the probability that a defect propagates silently. Instead of letting invalid state travel deeper into the system (where it becomes more expensive to debug), you:
- Detect anomalies early (fail fast)
- Localize responsibility for validation (single source of truth)
- Produce actionable failures (clear exception types + messages)
- Enable confident refactors (invariants checked near boundaries)

Think of it as designing *survivable* code: it still behaves predictably when inputs, dependencies, or environments misbehave.

### Choosing EAFP vs LBYL (A Practical Guide)
- Use **EAFP** when: natural Python exceptions already encode the failure (dict access, file I/O, attribute access, parsing). Cleaner, less branching.
- Use **LBYL** when: validation is cheaper/clearer than catching (e.g., numeric domain checks, protocol/shape verification) or when failure should raise a *different* semantic error than the low‑level one.
- Mix both thoughtfully: LBYL for *shaping* inputs → EAFP for *executing* operations.

Decision hints:
- Performance: LBYL may introduce TOCTTOU (time-of-check-to-time-of-use) race, especially with external resources—prefer EAFP there.
- Readability: If an if-chain is longer than the try/except clarity gain, prefer EAFP.
- Semantics: If you need to map low‑level errors to domain exceptions, catch then wrap.

### Assertions vs Exceptions
| Use | Prefer | Purpose |
|-----|--------|---------|
| Precondition violated by external caller | Exception (ValueError / TypeError / custom) | Communicate contract breach outward |
| Internal invariant that “must never happen” if code is correct | assert | Developer signal during testing & CI |
| User-facing recoverable condition | Exception | Allow caller to branch |
| Expensive condition in hot path (only in debug) | assert | Can be disabled with `-O` (don’t rely on for critical validation) |

Rule of thumb: If a malicious user could trigger it, don’t rely solely on `assert`—raise a real exception.

### Design by Contract in Python
Although Python has no native contract syntax, you can emulate contracts with:
1. Explicit validation (raise)
2. Assertions (internal dev checks)
3. Tests that exercise invalid + boundary inputs
4. Type hints + static analysis (mypy helps detect violations early)

Contract layers:
- Preconditions: Validate arguments before computing.
- Postconditions: Ensure result shape/value after computing.
- Invariants: Conditions that must always hold between public method calls.

### Designing Custom Exceptions
Good custom exceptions:
- Are *specific*: `InvalidEmailError` > `RegistrationError` > `Exception`
- Express **why** and optionally **what** (context, sanitized)
- Avoid leaking secrets (tokens, PII)
- Support structured handling (group base class → specific subclasses)

Patterns:
```python
class AppError(Exception):
    """Base for application-level errors."""

class ConfigError(AppError):
    pass

class MissingConfigKey(ConfigError):
    def __init__(self, key: str):
        super().__init__(f"Missing required config key: {key}")
```

### Input Validation Strategies
1. **Type validation**: `isinstance(x, (int, float))`
2. **Value domain**: range checks, membership, regex
3. **Structural**: required keys, lengths, optional fields
4. **Normalization before validation**: trim, lower, canonicalize locale forms
5. **Fail early**: return before touching deeper dependencies

Progressive example:
```python
def normalize_email(raw: str) -> str:
    if not isinstance(raw, str):
        raise TypeError("email must be str")
    email = raw.strip().lower()
    if "@" not in email or email.startswith("@"):
        raise ValueError(f"invalid email format: {raw!r}")
    return email
```

### Guard Clause Refactor Pattern
From this:
```python
if cond_a:
    if cond_b:
        if cond_c:
            return do_work()
        else:
            raise ...
```
To this:
```python
if not cond_a: raise ValueError("A failed")
if not cond_b: raise ValueError("B failed")
if not cond_c: raise ValueError("C failed")
return do_work()
```
Benefit: The *essential path* becomes the last 1–2 lines.

### Sentinel Values vs Exceptions
| Approach | Pros | Cons |
|----------|------|------|
| Return sentinel (None, -1) | Simpler call sites sometimes | Silent propagation; easy to forget checking |
| Raise exception | Forces handling / visibility | Slight overhead; must design types |
Prefer exceptions when the caller *must* react; use sentinel only when absence is genuinely normal (e.g., dict.get). Never overload multiple meanings onto `None`.

### Error Boundaries & Recovery
An error boundary isolates failures and prevents cascade. Techniques:
- Wrap integration points (network, file I/O) → convert to domain exceptions.
- Use **retry with backoff** only for transient errors (network/timeout, not logic bugs).
- Introduce a simple **circuit breaker** pattern when repeated failures occur (stop hammering dependency; degrade gracefully).

Pseudo-breaker:
```python
class Circuit:
    def __init__(self, failure_limit=5):
        self.failures = 0
        self.open = False
    def record_failure(self):
        self.failures += 1
        if self.failures >= 5: self.open = True
    def allow(self):
        return not self.open
```

### Logging Best Practices
DO:
- Include *what failed* + minimal sanitized context
- Use levels appropriately (INFO normal ops, WARNING recoverable anomaly, ERROR lost operation, CRITICAL system down)
- Log once per boundary (avoid duplicate stack trace spam)

AVOID:
- Logging sensitive data (passwords, tokens, full PII)
- Swallowing exceptions after logging without re-raising (unless intentionally recovering)
- Using broad bare `except:` — always narrow or at least `except Exception:`

### Testing Error Paths (Pytest Patterns)
```python
import pytest

def test_invalid_age():
    with pytest.raises(ValueError, match="negative"):
        process_user_age(-5)

def test_retry_exhaustion(monkeypatch):
    calls = {"n":0}
    def fail():
        calls["n"] += 1
        raise TimeoutError
    with pytest.raises(TimeoutError):
        retry_with_backoff(fail, max_attempts=3)
    assert calls["n"] == 3
```
Aim for: happy path, boundary, invalid type, invalid value, recovery scenario.

### Idempotency & Safety
Defensive functions should avoid irreversible side effects *before* validation completes. Strategies:
- Validate → transform → persist (never persist first)
- Use temp files, transactions, or staged writes
- Ensure retries are idempotent (PUT-like semantics, not duplicate inserts)

### Resource Safety (Context Managers)
Prefer context managers for anything that needs closing: files, locks, db connections. Combine with defensive checks to prevent leakage on exceptions.

### Quick Reference Checklist
- [ ] Inputs validated (type + domain)
- [ ] Guard clauses reduce nesting
- [ ] Meaningful custom exceptions used
- [ ] Assertions used only for internal invariants
- [ ] No bare `except:`
- [ ] Error messages actionable & sanitized
- [ ] Logging level appropriate
- [ ] Tests cover error + boundary conditions
- [ ] No silent sentinel misuse
- [ ] Resources always released

### Progressive Maturity Model
1. Reactive: Code breaks unexpectedly → manual debugging
2. Defensive: Early validation + clear exceptions
3. Contractual: Invariants & postconditions codified
4. Resilient: Recovery strategies (retry, fallback, circuit breaker)
5. Observability-driven: Metrics + structured logs → proactive improvement

Use this module to move from level 1–2 → 3–4.

## Verification

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
