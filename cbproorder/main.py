"""Application script."""
import cbpro

from cbproorder import settings
from cbproorder import utils
from cbproorder.logger import logger


def start(orders):
    """Authenticate with Coinbase and execute orders."""
    try:
        validate_orders(orders)
    except (ValueError, TypeError) as e:
        logger.error(
            "Unable to process request due to invalid order format",
            extra={"error": str(e), "orders": orders},
        )
        return

    try:
        auth_client = authenticate()
    except EnvironmentError:
        logger.error("There was an error loading your Coinbase credentials", exc_info=1)
        return

    result = {"success": [], "fail": []}

    for order in orders:
        response = auth_client.buy(
            product_id=order["product_id"],  # ex: BTC-USD
            order_type="market",
            # funds is the amount of 'quote currency' (RHS of the product_id pair) to buy
            funds=order["price"],
        )

        if not response:
            error = "Unable to connect to Coinbase Pro at this time. Please check your connectivity."
            logger.error(error, extra={"order": order})
            result["fail"].append({"order": order, "reason": error})
            continue

        if response.get("message"):
            error = response["message"]
            logger.error(error, extra={"order": order})
            result["fail"].append({"order": order, "reason": error})
            continue

        logger.info("Purchase successful", extra={"order": order})
        result["success"].append(order)

    return result


def validate_orders(orders):
    """Validate the incoming orders request.

    :raise: ValueError if orders values are invalid
    :raise: TypeError if orders types are invalid
    """
    if not orders:
        raise ValueError("No orders to validate")

    if not isinstance(orders, list):
        raise ValueError("Expected a list of orders")

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


def authenticate():
    """Create an authenticated client.

    Pulls configuration elements from environment variables and attempts to create an
    authenticated Coinbase client.

    :raise: EnvironmentError if Coinbase settings are missing
    :return: An authenticated Coinbase client
    :rtype: cbpro.AuthenticatedClient
    """
    coinbase = settings.CoinbaseConfig()

    if utils.is_local() or utils.is_dev():
        auth_client = cbpro.AuthenticatedClient(
            key=coinbase.API_KEY,
            b64secret=coinbase.API_SECRET,
            passphrase=coinbase.API_PASSPHRASE,
            api_url=coinbase.SANDBOX_API_URL,
        )
    else:
        auth_client = cbpro.AuthenticatedClient(
            key=coinbase.API_KEY,
            b64secret=coinbase.API_SECRET,
            passphrase=coinbase.API_PASSPHRASE,
        )

    return auth_client
