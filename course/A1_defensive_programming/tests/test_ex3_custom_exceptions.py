import pytest
from solutions.ex3_custom_exceptions import (
    UserRegistrationError,
    InvalidEmailError,
    WeakPasswordError,
    InvalidAgeError,
    UsernameUnavailableError,
    validate_email,
    validate_password,
    validate_age,
    register_user
)


class TestEmailValidation:
    """Test email validation function."""

    def test_valid_emails(self):
        """Test valid email formats."""
        valid_emails = [
            "user@example.com",
            "test.email@domain.org",
            "user123@test-domain.net",
            "name+tag@example.co.uk"
        ]

        for email in valid_emails:
            validate_email(email)  # Should not raise

    def test_invalid_emails(self):
        """Test invalid email formats."""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user@.com",
            "user@domain.",
            "user space@example.com",
            ""
        ]

        for email in invalid_emails:
            with pytest.raises(InvalidEmailError):
                validate_email(email)

    def test_email_type_validation(self):
        """Test that non-string inputs raise InvalidEmailError."""
        with pytest.raises(InvalidEmailError, match="Email must be a string"):
            validate_email(123)

        with pytest.raises(InvalidEmailError, match="Email must be a string"):
            validate_email(None)


class TestPasswordValidation:
    """Test password validation function."""

    def test_valid_passwords(self):
        """Test valid passwords."""
        valid_passwords = [
            "SecurePass123",
            "MyPassword1",
            "Test1234",
            "ComplexP@ssw0rd"
        ]

        for password in valid_passwords:
            validate_password(password)  # Should not raise

    def test_password_too_short(self):
        """Test password length requirement."""
        with pytest.raises(WeakPasswordError, match="at least 8 characters"):
            validate_password("Short1")

    def test_password_missing_uppercase(self):
        """Test uppercase letter requirement."""
        with pytest.raises(WeakPasswordError, match="uppercase letter"):
            validate_password("lowercase123")

    def test_password_missing_lowercase(self):
        """Test lowercase letter requirement."""
        with pytest.raises(WeakPasswordError, match="lowercase letter"):
            validate_password("UPPERCASE123")

    def test_password_missing_digit(self):
        """Test digit requirement."""
        with pytest.raises(WeakPasswordError, match="digit"):
            validate_password("NoDigitPassword")

    def test_password_type_validation(self):
        """Test that non-string inputs raise WeakPasswordError."""
        with pytest.raises(WeakPasswordError, match="Password must be a string"):
            validate_password(123456789)


class TestAgeValidation:
    """Test age validation function."""

    def test_valid_ages(self):
        """Test valid ages."""
        valid_ages = [13, 18, 25, 65, 100, 149]

        for age in valid_ages:
            validate_age(age)  # Should not raise

    def test_age_too_young(self):
        """Test minimum age requirement."""
        with pytest.raises(InvalidAgeError, match="at least 13 years old"):
            validate_age(12)

        with pytest.raises(InvalidAgeError, match="at least 13 years old"):
            validate_age(0)

    def test_age_too_old(self):
        """Test maximum age limit."""
        with pytest.raises(InvalidAgeError, match="less than 150"):
            validate_age(150)

        with pytest.raises(InvalidAgeError, match="less than 150"):
            validate_age(200)

    def test_age_type_validation(self):
        """Test that non-integer inputs raise InvalidAgeError."""
        with pytest.raises(InvalidAgeError, match="Age must be an integer"):
            validate_age("25")

        with pytest.raises(InvalidAgeError, match="Age must be an integer"):
            validate_age(25.5)


class TestUserRegistration:
    """Test complete user registration function."""

    def test_successful_registration(self):
        """Test successful user registration."""
        result = register_user("newuser", "new@example.com", "SecurePass123", 25)

        assert result["username"] == "newuser"
        assert result["email"] == "new@example.com"
        assert result["age"] == 25
        assert result["status"] == "registered"
        assert "created_at" in result

    def test_username_taken(self):
        """Test registration with existing username."""
        with pytest.raises(UsernameUnavailableError, match="already taken"):
            register_user("admin", "admin@example.com", "SecurePass123", 25)

    def test_empty_username(self):
        """Test registration with empty username."""
        with pytest.raises(UserRegistrationError, match="cannot be empty"):
            register_user("", "user@example.com", "SecurePass123", 25)

        with pytest.raises(UserRegistrationError, match="cannot be empty"):
            register_user("   ", "user@example.com", "SecurePass123", 25)

    def test_username_type_validation(self):
        """Test that non-string username raises error."""
        with pytest.raises(UserRegistrationError, match="Username must be a string"):
            register_user(123, "user@example.com", "SecurePass123", 25)

    def test_registration_with_invalid_email(self):
        """Test registration fails with invalid email."""
        with pytest.raises(InvalidEmailError):
            register_user("user", "invalid-email", "SecurePass123", 25)

    def test_registration_with_weak_password(self):
        """Test registration fails with weak password."""
        with pytest.raises(WeakPasswordError):
            register_user("user", "user@example.com", "weak", 25)

    def test_registration_with_invalid_age(self):
        """Test registration fails with invalid age."""
        with pytest.raises(InvalidAgeError):
            register_user("user", "user@example.com", "SecurePass123", 12)


class TestExceptionHierarchy:
    """Test custom exception hierarchy."""

    def test_exception_inheritance(self):
        """Test that all custom exceptions inherit from UserRegistrationError."""
        assert issubclass(InvalidEmailError, UserRegistrationError)
        assert issubclass(WeakPasswordError, UserRegistrationError)
        assert issubclass(InvalidAgeError, UserRegistrationError)
        assert issubclass(UsernameUnavailableError, UserRegistrationError)

    def test_base_exception_inheritance(self):
        """Test that UserRegistrationError inherits from Exception."""
        assert issubclass(UserRegistrationError, Exception)

    def test_catch_any_registration_error(self):
        """Test that UserRegistrationError can catch all registration errors."""
        with pytest.raises(UserRegistrationError):
            register_user("admin", "admin@example.com", "SecurePass123", 25)

        with pytest.raises(UserRegistrationError):
            register_user("user", "invalid-email", "SecurePass123", 25)

        with pytest.raises(UserRegistrationError):
            register_user("user", "user@example.com", "weak", 25)

        with pytest.raises(UserRegistrationError):
            register_user("user", "user@example.com", "SecurePass123", 12)
