import os
import unittest
from unittest.mock import patch

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
    @patch("coinbase.rest.RESTClient")
    @patch.dict(os.environ, {"COINBASE_API_BASE_URL": "http://test-url"})
    def test_init_with_env_var(self, mock_client):
        service = CoinbaseAdvancedService("test-api-key-name", "test-private-key")
        mock_client.assert_called_once_with(
            api_key="test-api-key-name",
            api_secret="test-private-key",
            base_url="http://test-url",
        )
        self.assertEqual(service.client, mock_client.return_value)

    @patch("coinbase.rest.RESTClient")
    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_env_var(self, mock_client):
        service = CoinbaseAdvancedService("test-api-key-name", "test-private-key")
        mock_client.assert_called_once_with(
            api_key="test-api-key-name",
            api_secret="test-private-key",
        )
        self.assertEqual(service.client, mock_client.return_value)

    @patch("coinbase.rest.RESTClient")
    @patch("uuid.uuid4")
    def test_create_buy_order_success(self, mock_uuid, mock_client):
        # Arrange
        order_id = "00000000-0000-0000-0000-000000000000"
        mock_uuid.return_value = order_id
        client = mock_client()
        client.market_order_buy.return_value = {
            "success": True,
            "order_id": "order_id",
            "success_response": {
                "order_id": "11111-00000-000000",
                "product_id": "BTC-USD",
                "side": "buy",
                "client_order_id": "0000-00000-000000",
            },
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": "100.0",
                    "base_size": "0.0",
                },
            },
        }
        coinbase = CoinbaseAdvancedService("api_key", "secret_key")
        coinbase.client = client
        order = Order(
            pair=Pair(base_currency="BTC", quote_currency="USD"),
            quote_size=100.0,
            side=OrderSide.BUY,
            type=OrderType.MARKET,
        )

        # Act
        actual_order_result = coinbase.create_market_buy_order(order=order)

        # Assert
        client.market_order_buy.assert_called_once_with(
            client_order_id=order_id,
            product_id=f"{order.pair.base_currency}-{order.pair.quote_currency}",
            quote_size=str(order.quote_size),
        )
        expected_order_result = OrderResult(
            success=True,
            order_id="order_id",
            product_id="BTC-USD",
            quote_size="100.0",
            base_size="0.0",
            side="buy",
        )
        self.assertEqual(
            expected_order_result,
            actual_order_result,
        )

    @patch("coinbaseadvanced.client.CoinbaseAdvancedTradeAPIClient")
    @patch("uuid.uuid4")
    def test_create_buy_order_failure(self, mock_uuid, mock_client):
        # Arrange
        mock_uuid.return_value = "00000000-0000-0000-0000-000000000000"
        client = mock_client()
        client.market_order_buy.return_value = {
            "success": False,
            "order_id": "order_id",
            "error_response": {
                "error": "INSUFFICIENT_FUND",
                "message": "Insufficient balance in source account",
                "error_details": "",
                "preview_failure_reason": "PREVIEW_INSUFFICIENT_FUND",
                "new_order_failure_reason": "UNKNOWN_FAILURE_REASON",
            },
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": "100.0",
                    "base_size": "0.0",
                },
            },
        }
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
        client.market_order_buy.assert_called_once_with(
            client_order_id="00000000-0000-0000-0000-000000000000",
            product_id=f"{order.pair.base_currency}-{order.pair.quote_currency}",
            quote_size=str(order.quote_size),
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
