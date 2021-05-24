"""Top-level main definition."""
from cbproorder import main
from cbproorder.logger import logger


if __name__ == "__main__":
    logger.debug("Starting application")
    # Temporary orders value for local sandbox testing
    orders = [{"product_id": "BTC-USD", "price": "10"}]
    main.start(orders)
