"""Application script."""
import cbpro

from cbproorder import settings
from cbproorder.logger import logger


def start(orders):
    """Authenticate with Coinbase and execute orders."""
    try:
        coinbase = settings.CoinbaseConfig()
    except EnvironmentError:
        logger.error("There was an error loading your Coinbase credentials", exc_info=1)
        return

    try:
        validate_orders(orders)
    except (ValueError, TypeError) as e:
        logger.error(f"Unable to process request due to invalid order format: {e}")
        return

    config = settings.Config()
    auth_client = cbpro.AuthenticatedClient(
        key=coinbase.API_KEY,
        b64secret=coinbase.API_SECRET,
        passphrase=coinbase.API_PASSPHRASE,
        api_url=config.SANDBOX_API_URL,
    )
    currencies = auth_client.get_currencies()
    logger.info(currencies)
    logger.info("done")


def validate_orders(orders):
    """Validate the incoming orders request."""
    if not orders:
        raise ValueError("No orders to validate")

    if not isinstance(orders, list):
        raise ValueError("Expected a list of orders")

    if not all(isinstance(order, dict) for order in orders):
        raise TypeError("Expected all orders to be a dictionary")

    if not all(isinstance(order, dict) for order in orders):
        raise TypeError("Expected all orders to be a dictionary")

    required_keys = ["price", "product_id"]

    if not all(
        [
            required_key in order.keys()
            for required_key in required_keys
            for order in orders
        ]
    ):
        raise ValueError(f"Each order must have the following keys: #{required_keys}")
