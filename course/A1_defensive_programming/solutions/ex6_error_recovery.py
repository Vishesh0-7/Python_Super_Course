import time
import logging
import random
import json
from typing import Optional, Any, Callable, List
from contextlib import contextmanager

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
    last_exception = None

    for attempt in range(max_attempts):
        try:
            logger.info(f"Attempt {attempt + 1} of {max_attempts}")
            result = func()
            logger.info(f"Success on attempt {attempt + 1}")
            return result
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1} failed: {e}")

            if attempt < max_attempts - 1:  # Don't sleep after last attempt
                delay = min(base_delay * (2 ** attempt), max_delay)
                logger.info(f"Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)

    logger.error(f"All {max_attempts} attempts failed")
    raise last_exception


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
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_file}")

            # Validate loaded config
            issues = self.validate_config()
            if issues:
                logger.warning(f"Configuration issues found: {issues}")

        except FileNotFoundError:
            logger.warning(f"Configuration file {self.config_file} not found, using defaults")
            self.config = self.defaults.copy()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {self.config_file}: {e}")
            logger.warning("Using default configuration")
            self.config = self.defaults.copy()
        except Exception as e:
            logger.error(f"Unexpected error loading config: {e}")
            logger.warning("Using default configuration")
            self.config = self.defaults.copy()

    def get(self, key: str, fallback: Any = None) -> Any:
        """
        Get configuration value with fallback.

        Args:
            key: Configuration key
            fallback: Value to return if key not found

        Returns:
            Configuration value or fallback
        """
        if key in self.config:
            return self.config[key]

        if fallback is not None:
            logger.debug(f"Using provided fallback for '{key}': {fallback}")
            return fallback

        if key in self.defaults:
            logger.debug(f"Using default value for '{key}': {self.defaults[key]}")
            return self.defaults[key]

        logger.warning(f"No value or default found for key '{key}'")
        return None

    def validate_config(self) -> List[str]:
        """
        Validate configuration and return list of issues.

        Returns:
            List of validation error messages
        """
        issues = []

        # Check cache_size is reasonable
        cache_size = self.config.get('cache_size')
        if cache_size is not None:
            if not isinstance(cache_size, int) or cache_size < 1:
                issues.append("cache_size must be a positive integer")

        # Check timeout is reasonable
        timeout = self.config.get('timeout')
        if timeout is not None:
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                issues.append("timeout must be a positive number")

        # Check debug is boolean
        debug = self.config.get('debug')
        if debug is not None and not isinstance(debug, bool):
            issues.append("debug must be a boolean")

        return issues


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
    file_handle = None
    try:
        file_handle = open(filename, mode)
        logger.debug(f"Successfully opened {filename} in mode '{mode}'")
        yield file_handle
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        yield None
    except PermissionError:
        logger.error(f"Permission denied accessing: {filename}")
        yield None
    except Exception as e:
        logger.error(f"Unexpected error with file {filename}: {e}")
        yield None
    finally:
        if file_handle:
            try:
                file_handle.close()
                logger.debug(f"Closed file: {filename}")
            except Exception as e:
                logger.error(f"Error closing file {filename}: {e}")


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
        processed_items = []

        logger.info(f"Processing {len(data)} data items")

        for i, item in enumerate(data):
            try:
                processed_item = self._process_single_item(item)
                processed_items.append(processed_item)
                logger.debug(f"Successfully processed item {i}")

            except Exception as e:
                self.error_count += 1
                logger.warning(f"Failed to process item {i}: {e}")

                # Check if we should degrade gracefully
                if self.error_count >= self.max_errors:
                    logger.error(f"Too many errors ({self.error_count}), stopping processing")
                    break

        success_rate = len(processed_items) / len(data) * 100
        logger.info(f"Processed {len(processed_items)}/{len(data)} items ({success_rate:.1f}% success)")

        return processed_items

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
        try:
            if key in self.cache:
                logger.debug(f"Cache hit for key: {key}")
                return self.cache[key]
            else:
                logger.debug(f"Cache miss for key: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache access error for key {key}: {e}")
            return None


def fetch_user_data(user_id: int) -> dict:
    """
    Fetch user data with comprehensive error handling.

    Args:
        user_id: ID of user to fetch

    Returns:
        User data dictionary with error recovery applied
    """
    # Fallback user data for when network is completely unavailable
    fallback_data = {
        "id": user_id,
        "name": "Guest User",
        "email": "guest@example.com",
        "status": "fallback",
        "last_seen": None
    }

    try:
        # Try to fetch real user data with retries
        logger.info(f"Fetching user data for user {user_id}")
        result = retry_with_backoff(
            lambda: unreliable_network_call(0.4),  # Low success rate to trigger retries
            max_attempts=3
        )

        # Transform network response to user data format
        user_data = {
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com",
            "status": "active",
            "last_seen": result["timestamp"]
        }

        logger.info(f"Successfully fetched user data for user {user_id}")
        return user_data

    except Exception as e:
        logger.error(f"Failed to fetch user data for user {user_id} after retries: {e}")
        logger.info(f"Returning fallback data for user {user_id}")
        return fallback_data
