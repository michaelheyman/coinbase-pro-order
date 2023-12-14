import uuid

from coinbaseadvanced import client
from coinbaseadvanced.models.orders import Order as CoinbaseAdvancedOrder

from cbproorder.domain.exception.order import UnsupportedOrderType
from cbproorder.domain.order_service import OrderService
from cbproorder.domain.value_object.orders import Order, OrderResult, OrderType


class CoinbaseAdvancedService(OrderService):
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

        return self._order_result_from_coinbase_advanced_order(
            order=order,
            coinbase_order=created_order,
        )

    def _order_result_from_coinbase_advanced_order(
        self,
        order: Order,
        coinbase_order: CoinbaseAdvancedOrder,
    ) -> OrderResult:
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
        success = True if coinbase_order.order_id and coinbase_order.side else False

        return OrderResult(
            success=success,
            order=order,
        )
