import os
from unittest import TestCase
from unittest.mock import patch

from cbproorder import settings


class CoinbaseAPI:
    """A set of test values for the Coinbase API"""

    key = "API key example"
    passphrase = "API passphrase example"
    secret = "API secret example"


def coinbase_api_dict():
    return {
        "API_KEY": CoinbaseAPI.key,
        "API_PASSPHRASE": CoinbaseAPI.passphrase,
        "API_SECRET": CoinbaseAPI.secret,
    }


class SettingsCoinbaseConfigTests(TestCase):
    @patch.dict(os.environ, coinbase_api_dict(), clear=True)
    def test_read_environment_variables(self):
        config = settings.CoinbaseConfig()

        self.assertEqual(CoinbaseAPI.key, config.api_key)
        self.assertEqual(CoinbaseAPI.passphrase, config.api_passphrase)
        self.assertEqual(CoinbaseAPI.secret, config.api_secret)

    @patch.dict(
        os.environ,
        {
            "API_PASSPHRASE": CoinbaseAPI.passphrase,
            "API_SECRET": CoinbaseAPI.secret,
        },
        clear=True,
    )
    def test_throws_exception_when_api_key_is_missing(self):
        try:
            settings.CoinbaseConfig()
            self.fail("Should have thrown exception")
        except EnvironmentError as e:
            self.assertTrue("API_KEY" in repr(e))

    @patch.dict(
        os.environ,
        {"API_KEY": CoinbaseAPI.key, "API_SECRET": CoinbaseAPI.secret},
        clear=True,
    )
    def test_throws_exception_when_api_passphrase_is_missing(self):
        try:
            settings.CoinbaseConfig()
            self.fail("Should have thrown exception")
        except EnvironmentError as e:
            self.assertTrue("API_PASSPHRASE" in repr(e))

    @patch.dict(
        os.environ,
        {"API_KEY": CoinbaseAPI.key, "API_PASSPHRASE": CoinbaseAPI.passphrase},
        clear=True,
    )
    def test_throws_exception_when_api_secret_is_missing(self):
        try:
            settings.CoinbaseConfig()
            self.fail("Should have thrown exception")
        except EnvironmentError as e:
            self.assertTrue("API_SECRET" in repr(e))
