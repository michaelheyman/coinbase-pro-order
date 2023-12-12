import uuid
from dataclasses import dataclass

from coinbaseadvanced import client
from coinbaseadvanced.models.orders import Order as CoinbaseAdvancedOrder

from cbproorder.application.order_service import OrderServiceInterface
from cbproorder.domain.exception.order import UnsupportedOrderType
from cbproorder.domain.value_object.orders import Order, OrderType


@dataclass
class OrderResult:
    """
    A class to represent the result of an order.

    Attributes:
        id (str): The ID of the order.
        product_id (str): The product ID of the order.
        side (str): The side of the order (buy or sell).
        type (str): The type of the order (limit, market, or stop).
        funds (float): The size of the order in quote currency.
        status (str): The status of the order.
    """

    # TODO: Add more attributes to this class.
    success: bool

    @classmethod
    def from_coinbase_advanced_order(cls, order: CoinbaseAdvancedOrder):
        """
        Create an OrderResult object from a CoinbaseAdvancedOrder object.

        The CoinbaseAdvancedOrder object is returned from the Coinbase Advanced
        Trade API, and its documentation can be found here:

        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder

        Args:
            order (CoinbaseAdvancedOrder): The CoinbaseAdvancedOrder object to convert.

        Returns:
            OrderResult: The converted OrderResult object.
        """
        success = True if order.order_id and order.side else False

        return cls(
            success=success,
        )


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

    def create_market_buy_order(self, order: Order) -> OrderResult:
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
        created_order = self.client.create_buy_market_order(
            client_order_id=client_order_id,
            product_id=product_id,
            quote_size=order.quote_size,
        )

        return OrderResult.from_coinbase_advanced_order(created_order)
