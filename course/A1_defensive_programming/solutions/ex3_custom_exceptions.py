import re


class UserRegistrationError(Exception):
    """Base exception for user registration errors."""
    pass


class InvalidEmailError(UserRegistrationError):
    """Raised when email format is invalid."""
    pass


class WeakPasswordError(UserRegistrationError):
    """Raised when password doesn't meet security requirements."""
    pass


class InvalidAgeError(UserRegistrationError):
    """Raised when age is invalid or user is too young."""
    pass


class UsernameUnavailableError(UserRegistrationError):
    """Raised when username is already taken."""
    pass


def validate_email(email):
    """
    Validate email format.

    Args:
        email (str): Email address to validate

    Raises:
        InvalidEmailError: If email format is invalid
    """
    if not isinstance(email, str):
        raise InvalidEmailError("Email must be a string")

    # Basic email validation - contains @ and has characters before and after
    email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    if not re.match(email_pattern, email):
        raise InvalidEmailError(f"Invalid email format: {email}")


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
    if not isinstance(password, str):
        raise WeakPasswordError("Password must be a string")

    if len(password) < 8:
        raise WeakPasswordError("Password must be at least 8 characters long")

    if not any(c.isupper() for c in password):
        raise WeakPasswordError("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        raise WeakPasswordError("Password must contain at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        raise WeakPasswordError("Password must contain at least one digit")


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
    if not isinstance(age, int):
        raise InvalidAgeError("Age must be an integer")

    if age < 13:
        raise InvalidAgeError("User must be at least 13 years old")

    if age >= 150:
        raise InvalidAgeError("Age must be less than 150")


# Existing users database (for username uniqueness checking)
EXISTING_USERS = {'admin', 'user123', 'testuser', 'john_doe'}


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
    # Validate username
    if not isinstance(username, str):
        raise UserRegistrationError("Username must be a string")

    if not username or len(username.strip()) == 0:
        raise UserRegistrationError("Username cannot be empty")

    if username in EXISTING_USERS:
        raise UsernameUnavailableError(f"Username '{username}' is already taken")

    # Validate all other fields
    validate_email(email)
    validate_password(password)
    validate_age(age)

    # If we get here, all validations passed
    return {
        "username": username,
        "email": email,
        "age": age,
        "status": "registered",
        "created_at": "2024-01-01T00:00:00Z"  # Simplified timestamp
    }
