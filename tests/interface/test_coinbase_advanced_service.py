import unittest
from unittest.mock import patch

# from cbproorder.coinbase import CoinbaseClient, CoinbaseFactory, OrderType
from cbproorder.interface.coinbase_advanced_service import CoinbaseAdvancedService
from cbproorder.domain.value_object.orders import Order, OrderSide, OrderType
from cbproorder.domain.value_object.pair import Pair


class TestCoinbaseClient(unittest.TestCase):
    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch("uuid.uuid4")
    def test_create_buy_order(self, mock_uuid, mock_client):
        # Arrange
        mock_uuid.return_value = "00000000-0000-0000-0000-000000000000"
        client = mock_client()
        client.create_buy_market_order.return_value = "order_id"
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
        self.assertEqual(result, "order_id")

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    def test_create_buy_order_unsupported_limit_order_type_returns_none(
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

        # Act
        result = coinbase.create_market_buy_order(order=order)

        # Assert
        self.assertEqual(result, None)

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    def test_create_buy_order_unsupported_stop_order_type_returns_none(
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

        # Act
        result = coinbase.create_market_buy_order(order=order)

        # Assert
        self.assertEqual(result, None)
