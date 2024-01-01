import os
import unittest
from unittest.mock import patch

from coinbaseadvanced.models.orders import Order as CoinbaseAdvancedOrder

from cbproorder.domain.exception.order import UnsupportedOrderType
from cbproorder.domain.value_object.orders import (
    Order,
    OrderResult,
    OrderSide,
    OrderType,
)
from cbproorder.domain.value_object.pair import Pair
from cbproorder.interface.coinbase_advanced_service import CoinbaseAdvancedService


class TestCoinbaseClient(unittest.TestCase):
    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch.dict(os.environ, {"COINBASE_API_BASE_URL": "http://test-url"})
    def test_init_with_env_var(self, mock_client):
        service = CoinbaseAdvancedService("test-api-key", "test-secret-key")
        mock_client.assert_called_once_with(
            api_key="test-api-key",
            secret_key="test-secret-key",
            base_url="http://test-url",
        )
        self.assertEqual(service.client, mock_client.return_value)

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_env_var(self, mock_client):
        service = CoinbaseAdvancedService("test-api-key", "test-secret-key")
        mock_client.assert_called_once_with(
            api_key="test-api-key",
            secret_key="test-secret-key",
        )
        self.assertEqual(service.client, mock_client.return_value)

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch("uuid.uuid4")
    def test_create_buy_order_success(self, mock_uuid, mock_client):
        # Arrange
        mock_uuid.return_value = "00000000-0000-0000-0000-000000000000"
        client = mock_client()
        client.create_buy_market_order.return_value = CoinbaseAdvancedOrder(
            order_id="order_id",
            product_id="BTC-USD",
            side="buy",
            client_order_id="client_order_id",
            order_configuration={
                "market_market_ioc": {
                    "quote_size": "100.0",
                    "base_size": "0.0",
                },
            },
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
        order_result = coinbase.create_market_buy_order(order=order)

        # Assert
        client.create_buy_market_order.assert_called_once_with(
            client_order_id="00000000-0000-0000-0000-000000000000",
            product_id=f"{order.pair.base_currency}-{order.pair.quote_currency}",
            quote_size=order.quote_size,
        )
        self.assertEqual(
            order_result,
            OrderResult(
                success=True,
                order_id="order_id",
                product_id="BTC-USD",
                quote_size="100.0",
                base_size="0.0",
                side="buy",
            ),
        )

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch("uuid.uuid4")
    def test_create_buy_order_failure(self, mock_uuid, mock_client):
        # Arrange
        mock_uuid.return_value = "00000000-0000-0000-0000-000000000000"
        client = mock_client()
        client.create_buy_market_order.return_value = CoinbaseAdvancedOrder(
            order_id="order_id",
            product_id="BTC-USD",
            side="buy",
            client_order_id="client_order_id",
            order_configuration={
                "market_market_ioc": {
                    "quote_size": "100.0",
                    "base_size": "0.0",
                },
            },
            order_error={
                "error": "INSUFFICIENT_FUND",
                "message": "Insufficient balance in source account",
                "error_details": "",
                "preview_failure_reason": "PREVIEW_INSUFFICIENT_FUND",
            },
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
        order_result = coinbase.create_market_buy_order(order=order)

        # Assert
        client.create_buy_market_order.assert_called_once_with(
            client_order_id="00000000-0000-0000-0000-000000000000",
            product_id=f"{order.pair.base_currency}-{order.pair.quote_currency}",
            quote_size=order.quote_size,
        )
        self.assertEqual(
            order_result,
            OrderResult(
                success=False,
                order_id="order_id",
                product_id="BTC-USD",
                error="INSUFFICIENT_FUND",
                error_message="Insufficient balance in source account",
                error_details="",
            ),
        )

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
