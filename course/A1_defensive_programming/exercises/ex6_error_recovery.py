"""
Exercise 6: Error Recovery and Graceful Degradation

Implement robust error handling with logging, fallback mechanisms, and graceful recovery.

Learn to write systems that:
- Fail gracefully rather than catastrophically
- Provide meaningful error messages and logging
- Implement fallback strategies when possible
- Maintain system stability under error conditions

Requirements:
- Implement retry mechanisms with exponential backoff
- Use proper logging to aid debugging
- Provide fallback values when appropriate
- Ensure resources are properly cleaned up
"""

import time
import logging
import random
from typing import Optional, Any, Callable, List
from contextlib import contextmanager

# Hint: Use logging instead of print for production error tracking
# Hint: Consider what operations should be retried vs fail immediately
# Hint: Think about resource cleanup and context managers
# Hint: Graceful degradation means reduced functionality, not complete failure

# Configure logging for this exercise
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NetworkError(Exception):
    """Simulated network error for testing."""
    pass


class ConfigurationError(Exception):
    """Configuration-related error."""
    pass


def unreliable_network_call(success_rate: float = 0.7) -> dict:
    """
    Simulate an unreliable network call for testing.

    Args:
        success_rate: Probability of success (0.0 to 1.0)

    Returns:
        dict: Simulated API response

    Raises:
        NetworkError: Randomly based on success_rate
    """
    if random.random() > success_rate:
        raise NetworkError("Simulated network failure")

    return {"status": "success", "data": "Important data", "timestamp": time.time()}


def retry_with_backoff(func: Callable, max_attempts: int = 3,
                      base_delay: float = 1.0, max_delay: float = 60.0) -> Any:
    """
    Retry a function with exponential backoff.

    Args:
        func: Function to retry (should take no arguments)
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay between attempts (seconds)
        max_delay: Maximum delay between attempts (seconds)

    Returns:
        Result of successful function call

    Raises:
        Exception: The last exception if all attempts fail
    """
    # TODO: Implement retry logic with exponential backoff
    # - Try the function
    # - If it fails, wait and try again with increasing delay
    # - Log each attempt and failure
    # - Raise the last exception if all attempts fail
    # - Calculate delay as: min(base_delay * (2 ** attempt), max_delay)
    pass


class ConfigManager:
    """
    Configuration manager with fallback and validation.
    """

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}
        self.defaults = {
            "database_url": "sqlite:///default.db",
            "cache_size": 100,
            "timeout": 30,
            "debug": False
        }
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration with fallback to defaults."""
        # TODO: Implement config loading with error recovery
        # - Try to load from file
        # - If file doesn't exist or is invalid, use defaults
        # - Log what happened (file loaded, using defaults, etc.)
        # - Validate loaded config values
        pass

    def get(self, key: str, fallback: Any = None) -> Any:
        """
        Get configuration value with fallback.

        Args:
            key: Configuration key
            fallback: Value to return if key not found

        Returns:
            Configuration value or fallback
        """
        # TODO: Implement safe config access
        # - Return config value if exists
        # - Return fallback if provided and key not found
        # - Return default if available and no fallback provided
        # - Log when fallbacks are used
        pass

    def validate_config(self) -> List[str]:
        """
        Validate configuration and return list of issues.

        Returns:
            List of validation error messages
        """
        # TODO: Implement config validation
        # Check for required keys, valid types, reasonable values, etc.
        # Return list of issues found (empty list if all good)
        pass


@contextmanager
def safe_file_operation(filename: str, mode: str = 'r'):
    """
    Context manager for safe file operations with proper cleanup.

    Args:
        filename: Path to file
        mode: File open mode

    Yields:
        File handle or None if operation failed
    """
    # TODO: Implement safe file context manager
    # - Try to open the file
    # - Yield file handle if successful, None if failed
    # - Ensure file is closed even if exception occurs
    # - Log any errors that occur
    pass


class DataProcessor:
    """
    Data processor with error recovery and graceful degradation.
    """

    def __init__(self, config: ConfigManager):
        self.config = config
        self.cache = {}
        self.error_count = 0
        self.max_errors = 5

    def process_data(self, data: List[dict]) -> List[dict]:
        """
        Process a list of data items with error recovery.

        Args:
            data: List of data items to process

        Returns:
            List of successfully processed items
        """
        # TODO: Implement robust data processing
        # - Process each item individually
        # - If an item fails, log error and continue with next item
        # - Track error count and degrade gracefully if too many errors
        # - Return all successfully processed items
        # - Use _process_single_item for individual processing
        pass

    def _process_single_item(self, item: dict) -> dict:
        """
        Process a single data item.

        Args:
            item: Data item to process

        Returns:
            Processed data item

        Raises:
            ValueError: If item is invalid
        """
        # Simulate processing that might fail
        if not isinstance(item, dict):
            raise ValueError(f"Expected dict, got {type(item)}")

        if "id" not in item:
            raise ValueError("Item missing required 'id' field")

        # Simulate random processing failure
        if random.random() < 0.2:  # 20% failure rate
            raise ValueError(f"Random processing failure for item {item.get('id')}")

        # Add processed timestamp
        processed_item = item.copy()
        processed_item["processed_at"] = time.time()
        processed_item["status"] = "processed"

        return processed_item

    def get_cached_data(self, key: str) -> Optional[Any]:
        """
        Get data from cache with error handling.

        Args:
            key: Cache key

        Returns:
            Cached data or None if not found/error
        """
        # TODO: Implement safe cache access
        # - Try to get from cache
        # - Return None if any error occurs
        # - Log cache hits/misses/errors
        pass


def fetch_user_data(user_id: int) -> dict:
    """
    Fetch user data with comprehensive error handling.

    Args:
        user_id: ID of user to fetch

    Returns:
        User data dictionary with error recovery applied
    """
    # TODO: Implement robust user data fetching
    # - Use retry_with_backoff for network call
    # - Provide fallback user data if network fails completely
    # - Log all attempts and outcomes
    # - Return either real data or fallback data, never None

    # Fallback user data for when network is completely unavailable
    fallback_data = {
        "id": user_id,
        "name": "Guest User",
        "email": "guest@example.com",
        "status": "fallback",
        "last_seen": None
    }

    pass


if __name__ == "__main__":
    print("=== Testing Retry Mechanism ===")
    try:
        # Test with low success rate to trigger retries
        result = retry_with_backoff(lambda: unreliable_network_call(0.3), max_attempts=3)
        print(f"Network call succeeded: {result}")
    except NetworkError as e:
        print(f"Network call failed after retries: {e}")

    print("\n=== Testing Configuration Manager ===")
    config = ConfigManager("nonexistent_config.json")
    print(f"Database URL: {config.get('database_url')}")
    print(f"Custom setting: {config.get('custom_setting', 'default_value')}")

    issues = config.validate_config()
    if issues:
        print(f"Config issues: {issues}")
    else:
        print("Configuration is valid")

    print("\n=== Testing Data Processing ===")
    processor = DataProcessor(config)

    # Test data with some invalid items
    test_data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        "invalid_item",  # This should be skipped
        {"name": "Charlie"},  # Missing ID, should be skipped
        {"id": 3, "name": "David"},
    ]

    processed = processor.process_data(test_data)
    print(f"Processed {len(processed)} out of {len(test_data)} items")

    print("\n=== Testing User Data Fetching ===")
    user_data = fetch_user_data(123)
    print(f"User data: {user_data}")

    print("\n=== Testing File Operations ===")
    with safe_file_operation("nonexistent_file.txt") as f:
        if f:
            content = f.read()
            print(f"File content: {content}")
        else:
            print("File operation failed, but handled gracefully")
