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

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_error_connectivity(self, _, mock_error_logger, mock_buy):
        mock_buy.return_value = None
        expected_error_message = "Unable to connect to Coinbase Pro at this time. Please check your connectivity."
        orders = [{"product_id": "BTC-USD", "price": "10.0"}]

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(expected_error_message)
        assert not result["success"]
        assert len(result["fail"]) == 1
        assert result["fail"][0] == {
            "order": orders[0],
            "reason": expected_error_message,
        }

    @patch("cbpro.AuthenticatedClient.buy")
    @patch("cbproorder.logger.logger.error")
    @patch("cbproorder.settings.CoinbaseConfig")
    def test_buy_error_funds_too_small(self, _, mock_error_logger, mock_buy):
        error_message = "funds is too small. Minimum size is 10.00000000"
        mock_buy.return_value = {"message": error_message}
        orders = [{"product_id": "BTC-USD", "price": "1.0"}]

        result = main.start(orders)

        mock_error_logger.assert_called_once_with(error_message)
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

        mock_error_logger.assert_called_once_with(error_message)
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

        mock_error_logger.assert_called_once_with(error_message)
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
        success_response = {
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
        mock_buy.return_value = success_response
        orders = [{"product_id": "BTC-USD", "price": "10.0"}]

        result = main.start(orders)

        mock_info_logger.assert_called_once_with("Purchase successful")
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
        success_response = {
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
        orders = [
            {"product_id": "BTC-USD", "price": "10.0"},
            {"product_id": "BTC-USD", "price": "exposure"},
            {"product_id": "BTC-USD", "price": "10.0"},
            {"product_id": "FOO-BAR", "price": "10.0"},
        ]
        errors = ["funds must be a number", "Product not found"]
        mock_buy.side_effect = [
            success_response,
            {"message": errors[0]},
            success_response,
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
