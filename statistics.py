"""Statistics tracker for Redis operations.

This module tracks operations performed on Redis and provides insights.
"""

import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class RedisStatistics:
    """Track statistics for Redis operations."""

    def __init__(self):
        self.operations = {
            "insert": 0,
            "update": 0,
            "search": 0,
            "delete": 0,
        }
        self.start_time = datetime.now()

    def record_operation(self, operation_type: str) -> None:
        """Record an operation of the specified type."""
        if operation_type in self.operations:
            self.operations[operation_type] += 1
            logger.debug(f"Recorded {operation_type} operation")

    def get_statistics(self) -> Dict[str, int]:
        """Get current statistics."""
        return self.operations.copy()

    def get_total_operations(self) -> int:
        """Get total number of operations."""
        return sum(self.operations.values())

    def print_summary(self) -> None:
        """Print a summary of operations."""
        runtime = datetime.now() - self.start_time
        logger.info("=== Redis Operations Summary ===")
        logger.info(f"Runtime: {runtime.total_seconds():.2f} seconds")
        logger.info(f"Total operations: {self.get_total_operations()}")
        for op, count in self.operations.items():
            logger.info(f"  {op}: {count}")
        logger.info("==============================")
