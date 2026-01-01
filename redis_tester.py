# redis_tester.py
from __future__ import annotations
import os
import json
import logging
import time
from typing import Optional, Any, Dict

import redis
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class AitRedisTester:
    def __init__(
        self,
        *,
        redis_client: Optional[redis.Redis] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        password: Optional[str] = None,
    ) -> None:
        """Initialize tester with either an injected client or env/config values.

        Priority:
        1) If redis_client is provided, use it.
        2) Else read host/port/password from args if provided.
        3) Else load from environment (.env supported).
        """
        # Load .env variables into the environment
        load_dotenv()

        self.r: Optional[redis.Redis] = redis_client
        self.host: Optional[str] = host or os.getenv("REDIS_HOST")
        self.port: int = int(
            port if port is not None else os.getenv("REDIS_PORT", 6379)
        )
        self.password: Optional[str] = (
            password if password is not None else os.getenv("REDIS_PASSWORD")
        )
        logger.info(f"Initializing with config for: {self.host}:{self.port}")

    def connect(self, max_retries: int = 3, retry_delay: float = 1.0) -> bool:
        """Establish a connection to the Redis server (or verify injected client).

        Args:
            max_retries: Maximum number of connection attempts (default: 3)
            retry_delay: Delay in seconds between retries (default: 1.0)
        """
        for attempt in range(1, max_retries + 1):
            try:
                # If a client was injected, just verify it
                if self.r is None:
                    # decode_responses=True makes sure we get strings back, not bytes
                    self.r = redis.Redis(
                        host=self.host,
                        port=self.port,
                        password=self.password,
                        decode_responses=True,
                        socket_timeout=5,  # Add 5 second timeout to prevent hanging
                        socket_connect_timeout=5,
                    )
                # Ping the server to test the connection
                self.r.ping()
                logger.info("✅ Successfully connected to Redis!")
                return True
            except redis.exceptions.ConnectionError as e:
                if attempt < max_retries:
                    logger.warning(f"Connection attempt {attempt}/{max_retries} failed. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"❌ Failed to connect to Redis after {max_retries} attempts: {e}")
                    return False
        return False

    def insert(self, key: str, value: Dict[str, Any]) -> bool:
        """Insert or update a JSON value for a given key (upsert)."""
        if not self.r:
            logger.warning("Not connected. Call connect() first.")
            return False

        try:
            json_value = json.dumps(value)
            self.r.set(key, json_value)
            logger.info(f"Successfully inserted/updated key: {key}")
            return True
        except Exception as e:
            logger.exception(f"Error during insert: {e}")
            return False

    def update(self, key: str, value: Dict[str, Any]) -> bool:
        """Alias of insert (Redis SET is an upsert)."""
        logger.info(f"Updating key '{key}' (same as insert)...")
        return self.insert(key, value)

    def search(self, key: str) -> Optional[Dict[str, Any]]:
        """Search for a key and return its JSON-deserialized value if present."""
        if not self.r:
            logger.warning("Not connected. Call connect() first.")
            return None

        try:
            json_value = self.r.get(key)
            if json_value:
                value = json.loads(json_value)
                logger.info(f"Found key: {key}")
                return value
            else:
                logger.info(f"Key not found: {key}")
                return None
        except Exception as e:
            logger.exception(f"Error during search: {e}")
            return None

    def delete(self, key: str) -> bool:
        """Delete a key from Redis. Returns True if a key was removed."""
        if not self.r:
            logger.warning("Not connected. Call connect() first.")
            return False

        try:
            result = self.r.delete(key)
            if result > 0:
                logger.info(f"Successfully deleted key: {key}")
                return True
            else:
                logger.info(f"Key not found to delete: {key}")
                return False
        except Exception as e:
            logger.exception(f"Error during delete: {e}")
            return False
