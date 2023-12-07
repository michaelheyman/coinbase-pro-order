import unittest
from unittest.mock import Mock, patch
from cbproorder.coinbase import CoinbaseClient, CoinbaseFactory, OrderType


class TestCoinbaseClient(unittest.TestCase):
    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch("uuid.uuid4")
    def test_create_buy_order(self, mock_uuid, mock_client):
        # Arrange
        mock_uuid.return_value = "00000000-0000-0000-0000-000000000000"
        client = mock_client()
        client.create_buy_market_order.return_value = "order_id"
        factory = CoinbaseFactory()
        coinbase = CoinbaseClient(factory, "api_key", "secret_key")
        coinbase.client = client

        # Act
        result = coinbase.create_buy_order("BTC-USD", OrderType.MARKET, 100.0)

        # Assert
        client.create_buy_market_order.assert_called_once_with(
            client_order_id="00000000-0000-0000-0000-000000000000",
            product_id="BTC-USD",
            quote_size=100.0,
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
        factory = CoinbaseFactory()
        coinbase = CoinbaseClient(factory, "api_key", "secret_key")
        coinbase.client = client

        # Act
        result = coinbase.create_buy_order("BTC-USD", OrderType.LIMIT, 100.0)

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
        factory = CoinbaseFactory()
        coinbase = CoinbaseClient(factory, "api_key", "secret_key")
        coinbase.client = client

        # Act
        result = coinbase.create_buy_order("BTC-USD", OrderType.STOP, 100.0)

        # Assert
        self.assertEqual(result, None)
