import uuid

from coinbaseadvanced import client

from cbproorder.application.order_service import OrderServiceInterface
from cbproorder.domain.exception.order import UnsupportedOrderType
from cbproorder.domain.value_object.orders import Order, OrderType


class CoinbaseAdvancedService(OrderServiceInterface):
    """
    A class to represent the Coinbase Advanced Service.

    This class is a concrete implementation of the OrderServiceInterface for the Coinbase Advanced API.

    Attributes:
        client (CoinbaseAdvancedTradeAPIClient): The client to interact with the Coinbase Advanced API.
    """

    def __init__(self, api_key: str, secret_key: str):
        """
        Constructs an instance of the CoinbaseAdvancedService.

        Args:
            api_key (str): The API key for the Coinbase Advanced Trade API.
            secret_key (str): The secret key for the Coinbase Advanced Trade API.
        """
        self.client = client.CoinbaseAdvancedTradeAPIClient(api_key, secret_key)

    # TODO: update this return type
    def create_market_buy_order(self, order: Order):
        """
        Create a buy type market order.

        Args:
            order (Order): The order to create a market buy order.

        Raises:
            UnsupportedOrderType: If the order type is not MARKET.

        Returns:
            dict: The response from the Coinbase Advanced API.
        """
        if order.type != OrderType.MARKET:
            raise UnsupportedOrderType(order.type)

        product_id = f"{order.pair.base_currency}-{order.pair.quote_currency}"
        client_order_id = str(uuid.uuid4())
        return self.client.create_buy_market_order(
            client_order_id=client_order_id,
            product_id=product_id,
            quote_size=order.quote_size,
        )
