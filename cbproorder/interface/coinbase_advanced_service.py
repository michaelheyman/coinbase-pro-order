import uuid

from coinbaseadvanced import client

from cbproorder.application.order_service import (
    OrderServiceInterface,
)
from cbproorder.domain.value_object.orders import Order, OrderType


class CoinbaseAdvancedService(OrderServiceInterface):
    def __init__(self, api_key: str, secret_key: str):
        self.client = client.CoinbaseAdvancedTradeAPIClient(api_key, secret_key)

    def create_market_buy_order(self, order: Order):
        """
        Create a buy type market order.

        Args:
        - product_id: The product this order was created for e.g. 'BTC-USD'.
        - order_type: The type of order to create. Must be a value in OrderType enum.
        - quote_size: Amount of quote currency to spend on order. Required for BUY orders.
        """

        if order.type != OrderType.MARKET:
            # Only market orders are supported at this time
            return None

        product_id = f"{order.pair.base_currency}-{order.pair.quote_currency}"
        client_order_id = str(uuid.uuid4())
        return self.client.create_buy_market_order(
            client_order_id=client_order_id,
            product_id=product_id,
            quote_size=order.quote_size,
        )
