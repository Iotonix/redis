"""Demo script for AitRedisTester.

Run a full CRUD flow on the APP_CONFIG key with statistics tracking.
"""

import json
import logging
from redis_tester import AitRedisTester
from statistics import RedisStatistics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Sample JSON object data for demonstration
# IMPORTANT: Replace with your actual configuration values
APP_CONFIG_DATA = {
    "_id": {"$oid": "507f1f77bcf86cd799439011"},
    "app_name": "DEMO-APP",
    "tenant": "DEMO",
    "logo_url": "https://example.com/logo.png",
    "dark_logo_url": "https://example.com/logo-dark.png",
    "favicon_url": "https://example.com/favicon.png",
    "login_background_url": "https://example.com/background.jpg",
    "primary_color": "#0066CC",
    "accent_color": "#666666",
    "server_ip": "https://api.example.com",
    "gf_api_key": "your-grafana-api-key-here",
    "google_api_key": "your-google-api-key-here",
}


def run_test():
    # 1. Create an instance of the tester and statistics tracker
    tester = AitRedisTester()
    stats = RedisStatistics()

    # 2. Connect to Redis
    if not tester.connect():
        # Stop if connection failed
        return

    logger.info("--- 🚀 Starting Redis Test ---")

    # 3. Insert the data
    logger.info("[TEST] Inserting data...")
    tester.insert("APP_CONFIG", APP_CONFIG_DATA)
    stats.record_operation("insert")

    # 4. Search for the data
    logger.info("[TEST] Searching for data...")
    retrieved_data = tester.search("APP_CONFIG")
    stats.record_operation("search")

    if retrieved_data:
        logger.info("Retrieved data:")
        logger.info(json.dumps(retrieved_data, indent=2))

    # Verify data (optional)
    if retrieved_data and retrieved_data.get("app_name") == "AIT-WEB":
        logger.info("✅ Data verification successful!")
    else:
        logger.warning("❌ Data verification failed!")

    # 5. Update the data
    logger.info("[TEST] Updating data...")
    updated_data = APP_CONFIG_DATA.copy()  # Make a copy to modify
    updated_data["primary_color"] = "#FF0000"  # Change a value
    tester.update("APP_CONFIG", updated_data)
    stats.record_operation("update")

    # Search again to confirm update
    logger.info("[TEST] Searching for updated data...")
    retrieved_updated_data = tester.search("APP_CONFIG")
    stats.record_operation("search")
    if retrieved_updated_data:
        logger.info(f"New primary_color: {retrieved_updated_data.get('primary_color')}")

    # 6. Delete the data (for cleanup)
    logger.info("[TEST] Deleting data...")
    tester.delete("APP_CONFIG")
    stats.record_operation("delete")

    # 7. Search one last time to confirm deletion
    logger.info("[TEST] Confirming deletion...")
    tester.search("APP_CONFIG")
    stats.record_operation("search")

    # 8. Insert the data again
    logger.info("[TEST] Inserting data again...")
    tester.insert("APP_CONFIG", APP_CONFIG_DATA)
    stats.record_operation("insert")

    # 9. Search one last time to confirm insertion
    logger.info("[TEST] Confirming insertion again...")
    tester.search("APP_CONFIG")
    stats.record_operation("search")

    logger.info("--- ✅ Test Complete ---")

    # Print statistics summary
    stats.print_summary()


if __name__ == "__main__":
    run_test()
