import uuid
from abc import ABC, abstractmethod
from enum import Enum

import coinbaseadvanced.client as advanced_client


class OrderType(Enum):
    """
    Enum representing supported order types.
    """

    LIMIT = "limit"
    MARKET = "market"
    STOP = "stop"


class ClientFactory(ABC):
    @abstractmethod
    def create_client(self, api_key: str, secret_key: str):
        pass


class CoinbaseFactory(ClientFactory):
    def create_client(self, api_key: str, secret_key: str):
        return advanced_client.CoinbaseAdvancedTradeAPIClient(api_key, secret_key)


class CoinbaseClient:
    def __init__(self, factory: ClientFactory, api_key: str, secret_key: str):
        self.client = factory.create_client(api_key, secret_key)

    def create_buy_order(
        self,
        product_id: str,
        order_type: OrderType,
        funds: float,
    ) -> advanced_client.Order:
        """
        Create a buy type market order.

        Args:
        - product_id: The product this order was created for e.g. 'BTC-USD'.
        - order_type: The type of order to create. Must be a value in OrderType enum.
        - quote_size: Amount of quote currency to spend on order. Required for BUY orders.
        """

        if order_type != OrderType.MARKET:
            # Only market orders are supported at this time
            return None

        client_order_id = str(uuid.uuid4())
        return self.client.create_buy_market_order(
            client_order_id=client_order_id,
            product_id=product_id,
            quote_size=funds,
        )
