from unittest import TestCase
from unittest.mock import patch

from cbproorder import main


class StartTests(TestCase):
    def setUp(self):
        self.success_response = {
            "id": "1c313a17-bf39-4c71-98b8-d58d3e706e9a",
            "product_id": "BTC-USD",
            "side": "buy",
            "stp": "dc",
            "funds": "9.95024875",
            "specified_funds": "10",
            "type": "market",
            "post_only": False,
            "created_at": "2021-05-24T03: 56: 28.091393Z",
            "fill_fees": "0",
            "filled_size": "0",
            "executed_value": "0",
            "status": "pending",
            "settled": False,
        }

    @patch("cbproorder.main.validate_orders")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_raises_exception_when_order_value_is_invalid(
        self, _, mock_error_logger, mock_validate_orders
    ):
        error = "value-error-message"
        mock_validate_orders.side_effect = ValueError(error)
        error_message = "Unable to process request due to invalid order format"
        orders = []

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(
            error_message, extra={"error": error, "orders": orders}
        )
        assert result is None

    @patch("cbproorder.main.validate_orders")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_raises_exception_when_order_type_is_invalid(
        self, _, mock_error_logger, mock_validate_orders
    ):
        error = "value-error-message"
        mock_validate_orders.side_effect = TypeError(error)
        error_message = "Unable to process request due to invalid order format"
        orders = ["product_id", "BTC-USD"]

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(
            error_message, extra={"error": error, "orders": orders}
        )
        assert result is None

    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.main.authenticate")
    @patch("cbproorder.main.validate_orders")
    def test_exits_when_config_raises_error(
        self, _, mock_authenticate, mock_error_logger
    ):
        mock_authenticate.side_effect = EnvironmentError
        error_message = "There was an error loading your Coinbase credentials"
        orders = []

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(error_message, exc_info=1)
        assert result is None

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_error_connectivity(self, _, mock_error_logger, mock_buy):
        error_message = "Unable to connect to Coinbase Pro at this time. Please check your connectivity."
        mock_buy.return_value = None
        orders = [{"product_id": "BTC-USD", "price": "10.0"}]

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(
            error_message, extra={"order": orders[0]}
        )
        assert not result["success"]
        assert len(result["fail"]) == 1
        assert result["fail"][0] == {
            "order": orders[0],
            "reason": error_message,
        }

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_error_funds_too_small(self, _, mock_error_logger, mock_buy):
        error_message = "funds is too small. Minimum size is 10.00000000"
        mock_buy.return_value = {"message": error_message}
        orders = [{"product_id": "BTC-USD", "price": "1.0"}]

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(
            error_message, extra={"order": orders[0]}
        )
        assert not result["success"]
        assert len(result["fail"]) == 1
        assert result["fail"][0] == {
            "order": orders[0],
            "reason": error_message,
        }

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_error_product_not_found(self, _, mock_error_logger, mock_buy):
        error_message = "Product not found"
        mock_buy.return_value = {"message": error_message}
        orders = [{"product_id": "FOO-BAR", "price": "10.0"}]

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(
            error_message, extra={"order": orders[0]}
        )
        assert not result["success"]
        assert len(result["fail"]) == 1
        assert result["fail"][0] == {
            "order": orders[0],
            "reason": error_message,
        }

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_error_funds_must_be_a_number(self, _, mock_error_logger, mock_buy):
        error_message = "funds must be a number"
        mock_buy.return_value = {"message": error_message}
        orders = [{"product_id": "BTC-USD", "price": "exposure"}]

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(
            error_message, extra={"order": orders[0]}
        )
        assert not result["success"]
        assert len(result["fail"]) == 1
        assert result["fail"][0] == {
            "order": orders[0],
            "reason": error_message,
        }

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.info")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_success(self, _, mock_info_logger, mock_buy):
        mock_buy.return_value = self.success_response
        orders = [{"product_id": "BTC-USD", "price": "10.0"}]

        result = main.start(orders)

        mock_info_logger.assert_called_once_with(
            "Purchase successful", extra={"order": orders[0]}
        )
        assert not result["fail"]
        assert len(result["success"]) == 1
        assert result["success"] == [orders[0]]

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.logger.logger.info")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_multiple_success_and_failure(
        self, _, mock_error_logger, mock_info_logger, mock_buy
    ):
        orders = [
            {"product_id": "BTC-USD", "price": "10.0"},
            {"product_id": "BTC-USD", "price": "exposure"},
            {"product_id": "BTC-USD", "price": "10.0"},
            {"product_id": "FOO-BAR", "price": "10.0"},
        ]
        errors = ["funds must be a number", "Product not found"]
        mock_buy.side_effect = [
            self.success_response,
            {"message": errors[0]},
            self.success_response,
            {"message": errors[1]},
        ]

        result = main.start(orders)

        assert mock_error_logger.call_count == 2
        assert mock_info_logger.call_count == 2
        assert len(result["success"]) == 2
        assert len(result["fail"]) == 2
        assert result["success"] == [orders[0], orders[2]]
        assert result["fail"] == [
            {"order": orders[1], "reason": errors[0]},
            {"order": orders[3], "reason": errors[1]},
        ]


class ValidateOrdersTests(TestCase):
    def test_empty_orders_raises_exception(self):
        orders = None

        with self.assertRaises(ValueError) as context:
            main.validate_orders(orders)
        self.assertEqual("No orders to validate", str(context.exception))

    def test_invalid_orders_collection_raises_exception(self):
        orders = {"product_id": "BTC-USD", "price": "10.0"}

        with self.assertRaises(ValueError) as context:
            main.validate_orders(orders)
        self.assertEqual("Expected a list of orders", str(context.exception))

        orders = "not-a-list"

        with self.assertRaises(ValueError) as context:
            main.validate_orders(orders)
        self.assertEqual("Expected a list of orders", str(context.exception))

    def test_invalid_orders_type_raises_exception(self):
        orders = [{"product_id": "BTC-USD", "price": "10.0"}, ["this-is-not-a-dict"]]

        with self.assertRaises(TypeError) as context:
            main.validate_orders(orders)
        self.assertEqual(
            "Expected all orders to be a dictionary", str(context.exception)
        )

    def test_invalid_order_keys_raises_exception(self):
        orders = [
            {
                # This is an example of a valid order
                "product_id": "BTC-USD",
                "price": "10.0",
            },
            {
                # This is not
                "this-is": "invalid",
                "and-so-is": "this",
            },
        ]
        self.assertRaises(ValueError, main.validate_orders, orders)


class AuthenticateTests(TestCase):
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_raises_exception_when_config_environment_variables_missing(
        self, mock_coinbase_config
    ):
        mock_coinbase_config.side_effect = EnvironmentError

        self.assertRaises(EnvironmentError, main.authenticate)

    @patch("cbproorder.settings.Config")
    @patch("cbproorder.settings.CoinbaseConfig")
    @patch("cbpro.AuthenticatedClient")
    def test_returns_authenticated_client(
        self, mock_auth_client, mock_coinbase_config, mock_config
    ):
        coinbase_config = mock_coinbase_config.return_value
        coinbase_config.API_KEY = "fake-api-key"
        coinbase_config.API_PASSPHRASE = "fake-passphrase"
        coinbase_config.API_SECRET = "fake-api-secret"
        config = mock_config.return_value
        config.SANDBOX_API_URL = "http://sandbox-api-url"
        authenticated_client = mock_auth_client.return_value
        authenticated_client.auth = "authenticated"

        auth_client = main.authenticate()

        mock_auth_client.assert_called_once_with(
            key=coinbase_config.API_KEY,
            b64secret=coinbase_config.API_SECRET,
            passphrase=coinbase_config.API_PASSPHRASE,
            api_url=config.SANDBOX_API_URL,
        )
        self.assertEqual(auth_client, authenticated_client)
