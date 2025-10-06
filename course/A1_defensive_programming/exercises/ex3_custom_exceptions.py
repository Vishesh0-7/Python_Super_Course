"""
Exercise 3: Custom Exceptions for Better Error Communication

Design and implement custom exceptions for a user registration system.

Create domain-specific exceptions that provide clear, actionable error messages
for different failure scenarios in user registration.

Requirements:
- Define custom exception classes for different error types
- Use inheritance to create a proper exception hierarchy
- Implement validation logic that raises appropriate custom exceptions
- Ensure error messages are helpful for both users and developers

Custom exceptions help you:
- Provide domain-specific error information
- Enable targeted error handling by callers
- Improve debugging and monitoring
- Separate concerns between different error types
"""

# Hint: Create a base exception class for your domain
# Hint: Inherit from appropriate built-in exception types
# Hint: Consider what information each exception should carry
# Hint: Think about who will handle these exceptions (user vs developer)

# TODO: Define your custom exception classes here
class UserRegistrationError(Exception):
    """Base exception for user registration errors."""
    pass

# TODO: Add more specific exception classes
# Consider: What specific things can go wrong during registration?
# - Invalid email format
# - Password not meeting requirements
# - Username already taken
# - Age restrictions
# - etc.


def validate_email(email):
    """
    Validate email format.

    Args:
        email (str): Email address to validate

    Raises:
        InvalidEmailError: If email format is invalid
    """
    # TODO: Implement email validation
    # Hint: Check for @ symbol, basic format validation
    pass


def validate_password(password):
    """
    Validate password strength.

    Args:
        password (str): Password to validate

    Raises:
        WeakPasswordError: If password doesn't meet requirements

    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    """
    # TODO: Implement password validation
    pass


def validate_age(age):
    """
    Validate user age.

    Args:
        age (int): User's age

    Raises:
        InvalidAgeError: If age is invalid or user is too young

    Requirements:
    - Must be at least 13 years old
    - Must be reasonable (< 150)
    """
    # TODO: Implement age validation
    pass


def register_user(username, email, password, age):
    """
    Register a new user with validation.

    Args:
        username (str): Desired username
        email (str): User's email address
        password (str): User's password
        age (int): User's age

    Returns:
        dict: User registration data

    Raises:
        UserRegistrationError: For any validation failure
    """
    # TODO: Implement user registration with all validations
    # Call the validation functions and handle the business logic
    # Return a dictionary with user data if all validations pass
    pass


# Existing users database (for username uniqueness checking)
EXISTING_USERS = {'admin', 'user123', 'testuser', 'john_doe'}


if __name__ == "__main__":
    # Quick manual tests
    test_cases = [
        ("newuser", "user@example.com", "SecurePass123", 25),  # Valid
        ("admin", "admin@example.com", "SecurePass123", 25),   # Username taken
        ("user2", "invalid-email", "SecurePass123", 25),       # Invalid email
        ("user3", "user3@example.com", "weak", 25),            # Weak password
        ("user4", "user4@example.com", "SecurePass123", 12),   # Too young
    ]

    for username, email, password, age in test_cases:
        try:
            result = register_user(username, email, password, age)
            print(f"✅ Registration successful: {result}")
        except Exception as e:
            print(f"❌ Registration failed: {type(e).__name__}: {e}")
