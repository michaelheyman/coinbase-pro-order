import unittest

from pydantic import ValidationError

from cbproorder.domain.value_object.orders import Order, OrderSide, OrderType


class TestOrder(unittest.TestCase):
    def test_from_dict_valid(self):
        order_dict = {
            "product_id": "ETH-USD",
            "price": 100.0,
        }
        order = Order.from_dict(order_dict)
        self.assertEqual(str(order.pair), "ETH-USD")
        self.assertEqual(order.quote_size, 100.0)
        self.assertEqual(order.side, OrderSide.BUY)
        self.assertEqual(order.type, OrderType.MARKET)

    def test_from_dict_invalid(self):
        order_dict = {
            "product_id": "ETH-USD",
            "price": 5.0,
        }
        with self.assertRaises(ValidationError):
            Order.from_dict(order_dict)
