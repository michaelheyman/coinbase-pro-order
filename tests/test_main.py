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

        result = main.start()

        assert result is None
        mock_error_logger.assert_called()


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
