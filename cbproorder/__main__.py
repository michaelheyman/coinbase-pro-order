"""Top-level main definition."""
from cbproorder import main
from cbproorder.logger import logger


if __name__ == "__main__":
    logger.debug("Starting application")
    orders = []
    main.start(orders)
