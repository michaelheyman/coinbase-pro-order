import unittest

from cbproorder.domain.value_object.pair import Pair


class TestPair(unittest.TestCase):
    def test_from_string_valid_input(self):
        pair = Pair.from_string("BTC-USD")
        self.assertEqual(pair.base_currency, "BTC")
        self.assertEqual(pair.quote_currency, "USD")

    def test_from_string_invalid_input(self):
        with self.assertRaises(ValueError):
            Pair.from_string("BTCUSD")

    def test_from_string_empty_input(self):
        with self.assertRaises(ValueError):
            Pair.from_string("")

    def test_str_representation(self):
        pair = Pair("BTC", "USD")
        self.assertEqual(str(pair), "BTC-USD")
