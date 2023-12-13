import unittest
from unittest.mock import patch

from coinbaseadvanced.models.orders import Order as CoinbaseAdvancedOrder

from cbproorder.domain.exception.order import UnsupportedOrderType
from cbproorder.domain.value_object.orders import Order, OrderSide, OrderType
from cbproorder.domain.value_object.pair import Pair
from cbproorder.interface.coinbase_advanced_service import CoinbaseAdvancedService


class TestCoinbaseClient(unittest.TestCase):
    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch("uuid.uuid4")
    def test_create_buy_order(self, mock_uuid, mock_client):
        # Arrange
        mock_uuid.return_value = "00000000-0000-0000-0000-000000000000"
        client = mock_client()
        client.create_buy_market_order.return_value = CoinbaseAdvancedOrder(
            product_id="BTC-USD",
            side="buy",
            client_order_id="client_order_id",
            order_configuration={},
            order_id="order_id",
        )
        coinbase = CoinbaseAdvancedService("api_key", "secret_key")
        coinbase.client = client
        order = Order(
            pair=Pair(base_currency="BTC", quote_currency="USD"),
            quote_size=100.0,
            side=OrderSide.BUY,
            type=OrderType.MARKET,
        )

        # Act
        result = coinbase.create_market_buy_order(order=order)

        # Assert
        client.create_buy_market_order.assert_called_once_with(
            client_order_id="00000000-0000-0000-0000-000000000000",
            product_id=f"{order.pair.base_currency}-{order.pair.quote_currency}",
            quote_size=order.quote_size,
        )
        self.assertEqual(result.success, True)

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    def test_create_buy_order_unsupported_limit_order_type_raises_unsupported_order_type_exception(
        self,
        mock_client,
    ):
        # Arrange
        client = mock_client()
        client.create_buy_market_order.return_value = "order_id"
        coinbase = CoinbaseAdvancedService("api_key", "secret_key")
        coinbase.client = client
        order = Order(
            pair=Pair(base_currency="BTC", quote_currency="USD"),
            quote_size=100.0,
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
        )

        # Act & Assert
        with self.assertRaises(UnsupportedOrderType):
            coinbase.create_market_buy_order(order=order),

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    def test_create_buy_order_unsupported_stop_order_type_raises_unsupported_order_type_exception(
        self,
        mock_client,
    ):
        # Arrange
        client = mock_client()
        client.create_buy_market_order.return_value = "order_id"
        coinbase = CoinbaseAdvancedService("api_key", "secret_key")
        coinbase.client = client
        order = Order(
            pair=Pair(base_currency="BTC", quote_currency="USD"),
            quote_size=100.0,
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
        )

        # Act & Assert
        with self.assertRaises(UnsupportedOrderType):
            coinbase.create_market_buy_order(order=order),
