from unittest import TestCase
from unittest.mock import patch

from cbproorder import main


class StartTests(TestCase):
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_exits_when_config_raises_error(
        self, mock_coinbase_config, mock_error_logger
    ):
        mock_coinbase_config.side_effect = EnvironmentError
        expected_error_message = "There was an error loading your Coinbase credentials"
        orders = []

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(expected_error_message, exc_info=1)
        assert result is None

    @patch("cbproorder.main.validate_orders")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_raises_exception_when_order_value_is_invalid(
        self, _, mock_error_logger, mock_validate_orders
    ):
        error_message = "value-error-message"
        mock_validate_orders.side_effect = ValueError(error_message)
        expected_error_message = (
            f"Unable to process request due to invalid order format: {error_message}"
        )
        orders = []

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(expected_error_message)
        assert result is None

    @patch("cbproorder.main.validate_orders")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_raises_exception_when_order_type_is_invalid(
        self, _, mock_error_logger, mock_validate_orders
    ):
        error_message = "value-error-message"
        mock_validate_orders.side_effect = TypeError(error_message)
        expected_error_message = (
            f"Unable to process request due to invalid order format: {error_message}"
        )
        orders = []

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(expected_error_message)
        assert result is None


class ValidateOrdersTests(TestCase):
    def test_empty_orders_raises_exception(self):
        orders = None
        self.assertRaises(ValueError, main.validate_orders, orders)

    def test_invalid_orders_collection_raises_exception(self):
        orders = {}
        self.assertRaises(ValueError, main.validate_orders, orders)
        orders = ""
        self.assertRaises(ValueError, main.validate_orders, orders)

    def test_invalid_orders_type_raises_exception(self):
        orders = [{"product_id": "BTC-USD", "price": "100.0"}, ["this-is-not-a-dict"]]
        self.assertRaises(TypeError, main.validate_orders, orders)

    def test_invalid_order_keys_raises_exception(self):
        orders = [
            {
                # This is an example of a valid order
                "product_id": "BTC-USD",
                "price": "100.0",
            },
            {
                # This is not
                "this-is": "invalid",
                "and-so-is": "this",
            },
        ]
        self.assertRaises(ValueError, main.validate_orders, orders)
