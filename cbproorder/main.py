"""Application script."""
from cbproorder import coinbase
from cbproorder import settings
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
        config = settings.CoinbaseConfig()
        client = coinbase.CoinbaseClient(
            coinbase.CoinbaseFactory(),
            config.API_KEY,
            config.API_SECRET,
        )
    except EnvironmentError:
        logger.error("There was an error loading your Coinbase credentials", exc_info=1)
        return

    result = {"success": [], "fail": []}

    for order in orders:
        response = client.create_buy_order(
            product_id=order["product_id"],  # ex: BTC-USD
            order_type=coinbase.OrderType.MARKET,
            # funds is the amount of 'quote currency' (RHS of the product_id pair) to buy
            funds=order["price"],
        )

        if not response:
            error = "Unable to connect to Coinbase at this time. Please check your connectivity."
            logger.error(error, extra={"order": order})
            result["fail"].append({"order": order, "reason": error})
            continue

        if response.order_error:
            error = response.order_error.message
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
