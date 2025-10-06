import pytest
import json
import tempfile
import os
import time
from unittest.mock import patch, MagicMock
from solutions.ex6_error_recovery import (
    NetworkError,
    ConfigurationError,
    unreliable_network_call,
    retry_with_backoff,
    ConfigManager,
    safe_file_operation,
    DataProcessor,
    fetch_user_data
)


class TestRetryWithBackoff:
    """Test retry mechanism with exponential backoff."""

    def test_successful_first_attempt(self):
        """Test function succeeding on first attempt."""
        mock_func = MagicMock(return_value="success")

        result = retry_with_backoff(mock_func, max_attempts=3)

        assert result == "success"
        assert mock_func.call_count == 1

    def test_success_after_retries(self):
        """Test function succeeding after failures."""
        call_count = 0

        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise NetworkError("Simulated failure")
            return "success"

        with patch('time.sleep'):  # Mock sleep to speed up test
            result = retry_with_backoff(failing_func, max_attempts=3)

        assert result == "success"
        assert call_count == 3

    def test_all_attempts_fail(self):
        """Test when all retry attempts fail."""
        def always_failing_func():
            raise NetworkError("Always fails")

        with patch('time.sleep'):  # Mock sleep to speed up test
            with pytest.raises(NetworkError, match="Always fails"):
                retry_with_backoff(always_failing_func, max_attempts=2)

    def test_exponential_backoff_timing(self):
        """Test that delays follow exponential backoff pattern."""
        def always_failing_func():
            raise NetworkError("Always fails")

        with patch('time.sleep') as mock_sleep:
            with pytest.raises(NetworkError):
                retry_with_backoff(always_failing_func, max_attempts=3, base_delay=1.0)

            # Should sleep twice (between attempts 1-2 and 2-3)
            assert mock_sleep.call_count == 2

            # Check exponential backoff: 1.0, 2.0
            calls = mock_sleep.call_args_list
            assert calls[0][0][0] == 1.0  # First delay
            assert calls[1][0][0] == 2.0  # Second delay

    def test_max_delay_limit(self):
        """Test that delay doesn't exceed max_delay."""
        def always_failing_func():
            raise NetworkError("Always fails")

        with patch('time.sleep') as mock_sleep:
            with pytest.raises(NetworkError):
                retry_with_backoff(
                    always_failing_func,
                    max_attempts=4,
                    base_delay=10.0,
                    max_delay=15.0
                )

            # Check that delays don't exceed max_delay
            for call in mock_sleep.call_args_list:
                assert call[0][0] <= 15.0


class TestConfigManager:
    """Test configuration manager with fallback capabilities."""

    def test_valid_config_loading(self):
        """Test loading valid configuration file."""
        config_data = {
            "database_url": "postgresql://localhost/mydb",
            "cache_size": 200,
            "timeout": 60,
            "debug": True
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_file = f.name

        try:
            config = ConfigManager(temp_file)
            assert config.get('database_url') == "postgresql://localhost/mydb"
            assert config.get('cache_size') == 200
            assert config.get('timeout') == 60
            assert config.get('debug') is True
        finally:
            os.unlink(temp_file)

    def test_missing_config_file(self):
        """Test fallback when config file is missing."""
        config = ConfigManager("nonexistent_file.json")

        # Should use defaults
        assert config.get('database_url') == "sqlite:///default.db"
        assert config.get('cache_size') == 100
        assert config.get('timeout') == 30
        assert config.get('debug') is False

    def test_invalid_json_file(self):
        """Test fallback when config file has invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_file = f.name

        try:
            config = ConfigManager(temp_file)

            # Should use defaults due to JSON error
            assert config.get('database_url') == "sqlite:///default.db"
            assert config.get('cache_size') == 100
        finally:
            os.unlink(temp_file)

    def test_get_with_fallback(self):
        """Test get method with custom fallbacks."""
        config = ConfigManager("nonexistent_file.json")

        # Test custom fallback
        assert config.get('custom_key', 'my_fallback') == 'my_fallback'

        # Test default fallback
        assert config.get('cache_size') == 100

        # Test no fallback or default
        assert config.get('unknown_key') is None

    def test_config_validation(self):
        """Test configuration validation."""
        # Valid config
        valid_config_data = {
            "cache_size": 200,
            "timeout": 30.0,
            "debug": True
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_config_data, f)
            temp_file = f.name

        try:
            config = ConfigManager(temp_file)
            issues = config.validate_config()
            assert len(issues) == 0
        finally:
            os.unlink(temp_file)

        # Invalid config
        invalid_config_data = {
            "cache_size": -10,  # Invalid: negative
            "timeout": "30",    # Invalid: string instead of number
            "debug": "yes"      # Invalid: string instead of boolean
        }

        config = ConfigManager("nonexistent_file.json")
        config.config = invalid_config_data

        issues = config.validate_config()
        assert len(issues) > 0
        assert any("cache_size" in issue for issue in issues)
        assert any("timeout" in issue for issue in issues)
        assert any("debug" in issue for issue in issues)


class TestSafeFileOperation:
    """Test safe file operation context manager."""

    def test_successful_file_operation(self):
        """Test successful file read/write operations."""
        test_content = "Hello, World!"

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(test_content)
            temp_file = f.name

        try:
            # Test reading
            with safe_file_operation(temp_file, 'r') as f:
                assert f is not None
                content = f.read()
                assert content == test_content
        finally:
            os.unlink(temp_file)

    def test_missing_file(self):
        """Test handling of missing file."""
        with safe_file_operation("nonexistent_file.txt", 'r') as f:
            assert f is None

    def test_permission_error(self):
        """Test handling of permission errors."""
        # Create a file and make it unreadable (Unix-like systems)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name

        try:
            # Make file unreadable
            os.chmod(temp_file, 0o000)

            with safe_file_operation(temp_file, 'r') as f:
                # Should handle permission error gracefully
                assert f is None
        finally:
            # Restore permissions and clean up
            os.chmod(temp_file, 0o644)
            os.unlink(temp_file)

    def test_file_cleanup(self):
        """Test that files are properly closed even on exceptions."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_file = f.name

        try:
            with safe_file_operation(temp_file, 'r') as f:
                assert f is not None
                # File should be automatically closed when context exits
                pass

            # File should be closed now
            assert f.closed
        finally:
            os.unlink(temp_file)


class TestDataProcessor:
    """Test data processor with error recovery."""

    def setup_method(self):
        """Set up test data processor."""
        config = ConfigManager("nonexistent_file.json")  # Uses defaults
        self.processor = DataProcessor(config)

    def test_successful_data_processing(self):
        """Test processing valid data items."""
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"}
        ]

        with patch('random.random', return_value=0.9):  # Prevent random failures
            processed = self.processor.process_data(data)

        assert len(processed) == 3
        for i, item in enumerate(processed):
            assert item["id"] == i + 1
            assert "processed_at" in item
            assert item["status"] == "processed"

    def test_error_recovery(self):
        """Test that processing continues after individual item failures."""
        data = [
            {"id": 1, "name": "Alice"},  # Valid
            "invalid_item",              # Invalid: not a dict
            {"name": "Bob"},             # Invalid: missing id
            {"id": 4, "name": "David"}   # Valid
        ]

        with patch('random.random', return_value=0.9):  # Prevent random failures
            processed = self.processor.process_data(data)

        # Should process 2 out of 4 items
        assert len(processed) == 2
        assert processed[0]["id"] == 1
        assert processed[1]["id"] == 4

    def test_graceful_degradation(self):
        """Test graceful degradation when too many errors occur."""
        # Create data that will cause many errors
        data = [{"id": i} for i in range(10)]

        # Force random failures to trigger degradation
        with patch('random.random', return_value=0.1):  # High failure rate
            processed = self.processor.process_data(data)

        # Should stop processing after max_errors
        assert len(processed) < len(data)
        assert self.processor.error_count >= self.processor.max_errors

    def test_cache_operations(self):
        """Test safe cache operations."""
        # Test cache miss
        result = self.processor.get_cached_data("missing_key")
        assert result is None

        # Test cache hit
        self.processor.cache["test_key"] = "test_value"
        result = self.processor.get_cached_data("test_key")
        assert result == "test_value"


class TestFetchUserData:
    """Test user data fetching with comprehensive error handling."""

    def test_successful_user_fetch(self):
        """Test successful user data fetching."""
        with patch('solutions.ex6_error_recovery.unreliable_network_call') as mock_call:
            mock_call.return_value = {
                "status": "success",
                "data": "user data",
                "timestamp": 1234567890
            }

            user_data = fetch_user_data(123)

            assert user_data["id"] == 123
            assert user_data["name"] == "User 123"
            assert user_data["status"] == "active"
            assert user_data["last_seen"] == 1234567890

    def test_fallback_on_network_failure(self):
        """Test fallback when network completely fails."""
        with patch('solutions.ex6_error_recovery.retry_with_backoff') as mock_retry:
            mock_retry.side_effect = NetworkError("Network unavailable")

            user_data = fetch_user_data(456)

            # Should return fallback data
            assert user_data["id"] == 456
            assert user_data["name"] == "Guest User"
            assert user_data["status"] == "fallback"
            assert user_data["last_seen"] is None

    def test_retry_mechanism_called(self):
        """Test that retry mechanism is properly invoked."""
        with patch('solutions.ex6_error_recovery.retry_with_backoff') as mock_retry:
            mock_retry.return_value = {
                "status": "success",
                "timestamp": 1234567890
            }

            fetch_user_data(789)

            # Verify retry was called with correct parameters
            mock_retry.assert_called_once()
            args, kwargs = mock_retry.call_args
            assert kwargs.get('max_attempts', 3) == 3


class TestUnreliableNetworkCall:
    """Test the simulated unreliable network call."""

    def test_success_case(self):
        """Test successful network call."""
        with patch('random.random', return_value=0.3):  # Below success rate
            result = unreliable_network_call(0.7)

            assert result["status"] == "success"
            assert "data" in result
            assert "timestamp" in result

    def test_failure_case(self):
        """Test failed network call."""
        with patch('random.random', return_value=0.8):  # Above success rate
            with pytest.raises(NetworkError, match="Simulated network failure"):
                unreliable_network_call(0.7)
