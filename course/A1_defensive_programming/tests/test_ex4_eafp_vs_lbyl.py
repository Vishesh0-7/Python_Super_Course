import pytest
import json
import tempfile
import os
from solutions.ex4_eafp_vs_lbyl import (
    safe_get_nested_value,
    validate_numeric_range,
    load_config_file,
    calculate_bmi,
    get_user_preference,
    parse_integer_list
)


class TestSafeGetNestedValue:
    """Test EAFP approach for nested dictionary access."""

    def test_valid_nested_access(self):
        """Test successful nested value retrieval."""
        data = {
            "user": {
                "profile": {"name": "Alice", "age": 30},
                "settings": {"theme": "dark", "notifications": True}
            },
            "system": {"version": "1.0"}
        }

        assert safe_get_nested_value(data, "user.profile.name") == "Alice"
        assert safe_get_nested_value(data, "user.profile.age") == 30
        assert safe_get_nested_value(data, "user.settings.theme") == "dark"
        assert safe_get_nested_value(data, "system.version") == "1.0"

    def test_missing_keys(self):
        """Test handling of missing keys."""
        data = {"user": {"profile": {"name": "Alice"}}}

        assert safe_get_nested_value(data, "user.profile.missing") is None
        assert safe_get_nested_value(data, "user.missing.field") is None
        assert safe_get_nested_value(data, "missing.key.path") is None

    def test_single_level_access(self):
        """Test single-level key access."""
        data = {"key": "value", "number": 42}

        assert safe_get_nested_value(data, "key") == "value"
        assert safe_get_nested_value(data, "number") == 42
        assert safe_get_nested_value(data, "missing") is None

    def test_empty_data(self):
        """Test with empty dictionary."""
        assert safe_get_nested_value({}, "any.key") is None

    def test_type_errors(self):
        """Test handling when intermediate values are not dictionaries."""
        data = {"user": "not_a_dict"}
        assert safe_get_nested_value(data, "user.profile.name") is None


class TestValidateNumericRange:
    """Test LBYL approach for numeric validation."""

    def test_valid_numbers(self):
        """Test valid numeric inputs."""
        assert validate_numeric_range(25, 0, 100) == 25.0
        assert validate_numeric_range(0, 0, 100) == 0.0
        assert validate_numeric_range(100, 0, 100) == 100.0
        assert validate_numeric_range(50.5, 0, 100) == 50.5

    def test_type_errors(self):
        """Test type validation."""
        with pytest.raises(TypeError, match="Value must be numeric"):
            validate_numeric_range("25", 0, 100)

        with pytest.raises(TypeError, match="Value must be numeric"):
            validate_numeric_range(None, 0, 100)

        with pytest.raises(TypeError, match="Value must be numeric"):
            validate_numeric_range([25], 0, 100)

    def test_range_errors(self):
        """Test range validation."""
        with pytest.raises(ValueError, match="below minimum"):
            validate_numeric_range(-5, 0, 100)

        with pytest.raises(ValueError, match="above maximum"):
            validate_numeric_range(150, 0, 100)

    def test_boundary_values(self):
        """Test boundary conditions."""
        # Exact boundaries should be valid
        assert validate_numeric_range(0, 0, 100) == 0.0
        assert validate_numeric_range(100, 0, 100) == 100.0

        # Just outside boundaries should fail
        with pytest.raises(ValueError):
            validate_numeric_range(-0.1, 0, 100)

        with pytest.raises(ValueError):
            validate_numeric_range(100.1, 0, 100)


class TestLoadConfigFile:
    """Test EAFP approach for file operations."""

    def test_valid_json_file(self):
        """Test loading valid JSON configuration."""
        config_data = {"database_url": "sqlite:///test.db", "debug": True}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_file = f.name

        try:
            result = load_config_file(temp_file)
            assert result == config_data
        finally:
            os.unlink(temp_file)

    def test_missing_file(self):
        """Test handling of missing file."""
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            load_config_file("nonexistent_file.json")

    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_file = f.name

        try:
            with pytest.raises(json.JSONDecodeError, match="Invalid JSON"):
                load_config_file(temp_file)
        finally:
            os.unlink(temp_file)

    def test_empty_file(self):
        """Test handling of empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                load_config_file(temp_file)
        finally:
            os.unlink(temp_file)


class TestCalculateBMI:
    """Test hybrid LBYL/EAFP approach for BMI calculation."""

    def test_valid_bmi_calculations(self):
        """Test valid BMI calculations."""
        # Normal BMI
        assert abs(calculate_bmi(70, 1.75) - 22.86) < 0.01

        # Underweight BMI
        assert abs(calculate_bmi(50, 1.75) - 16.33) < 0.01

        # Overweight BMI
        assert abs(calculate_bmi(90, 1.75) - 29.39) < 0.01

    def test_type_validation(self):
        """Test type validation (LBYL)."""
        with pytest.raises(TypeError, match="Weight must be numeric"):
            calculate_bmi("70", 1.75)

        with pytest.raises(TypeError, match="Height must be numeric"):
            calculate_bmi(70, "1.75")

    def test_value_validation(self):
        """Test value validation (LBYL)."""
        with pytest.raises(ValueError, match="Weight must be positive"):
            calculate_bmi(-70, 1.75)

        with pytest.raises(ValueError, match="Height must be positive"):
            calculate_bmi(70, -1.75)

        with pytest.raises(ValueError, match="Height must be positive"):
            calculate_bmi(70, 0)

    def test_edge_cases(self):
        """Test edge cases."""
        # Very small but positive values
        result = calculate_bmi(0.1, 0.1)
        assert result > 0

        # Large values
        result = calculate_bmi(200, 2.5)
        assert result > 0


class TestGetUserPreference:
    """Test EAFP approach for preference access."""

    def test_valid_preferences(self):
        """Test successful preference retrieval."""
        user_data = {
            "preferences": {
                "theme": "dark",
                "language": "en",
                "notifications": True
            }
        }

        assert get_user_preference(user_data, "theme") == "dark"
        assert get_user_preference(user_data, "language") == "en"
        assert get_user_preference(user_data, "notifications") is True

    def test_missing_preferences(self):
        """Test handling of missing preferences."""
        user_data = {"preferences": {"theme": "dark"}}

        assert get_user_preference(user_data, "missing") is None
        assert get_user_preference(user_data, "missing", "default") == "default"

    def test_missing_preferences_section(self):
        """Test handling when preferences section is missing."""
        user_data = {"name": "Alice"}

        assert get_user_preference(user_data, "theme") is None
        assert get_user_preference(user_data, "theme", "light") == "light"

    def test_invalid_user_data(self):
        """Test handling of invalid user data structure."""
        # Not a dictionary
        assert get_user_preference("not_a_dict", "theme") is None
        assert get_user_preference(None, "theme", "default") == "default"


class TestParseIntegerList:
    """Test EAFP approach for string parsing."""

    def test_valid_integer_lists(self):
        """Test parsing valid integer strings."""
        assert parse_integer_list("1,2,3,4") == [1, 2, 3, 4]
        assert parse_integer_list("10, 20, 30") == [10, 20, 30]  # With spaces
        assert parse_integer_list("-1,0,1") == [-1, 0, 1]  # Negative numbers
        assert parse_integer_list("42") == [42]  # Single number

    def test_empty_string(self):
        """Test parsing empty string."""
        assert parse_integer_list("") == []
        assert parse_integer_list("   ") == []  # Only whitespace

    def test_invalid_integers(self):
        """Test handling of invalid integers."""
        with pytest.raises(ValueError, match="Invalid integer"):
            parse_integer_list("1,2,abc,4")

        with pytest.raises(ValueError, match="Invalid integer"):
            parse_integer_list("1,2.5,3")  # Float

        with pytest.raises(ValueError, match="Invalid integer"):
            parse_integer_list("1,,3")  # Empty item

    def test_whitespace_handling(self):
        """Test proper whitespace handling."""
        assert parse_integer_list(" 1 , 2 , 3 ") == [1, 2, 3]
        assert parse_integer_list("1,\t2,\n3") == [1, 2, 3]
