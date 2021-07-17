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
    def test_read_coinbase_environment_variables(self):
        config = settings.CoinbaseConfig()

        self.assertEqual(CoinbaseAPI.key, config.API_KEY)
        self.assertEqual(CoinbaseAPI.passphrase, config.API_PASSPHRASE)
        self.assertEqual(CoinbaseAPI.secret, config.API_SECRET)

    @patch.dict(os.environ, coinbase_api_dict(), clear=True)
    def test_hardcoded_sandox_api_url(self):
        config = settings.CoinbaseConfig()

        self.assertEqual(
            "https://api-public.sandbox.pro.coinbase.com", config.SANDBOX_API_URL
        )

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


class SettingsConfigTests(TestCase):
    @patch.dict(os.environ, {"LOGGING_LEVEL": "DEBUG"})
    def test_read_logging_environment_variable(self):
        config = settings.Config()

        self.assertEqual("DEBUG", config.LOGGING_LEVEL)

    @patch.dict(os.environ, {}, clear=True)
    def test_read_missing_logging_environment_variable_defaults_to_info(self):
        config = settings.Config()

        self.assertEqual("INFO", config.LOGGING_LEVEL)

    @patch.dict(os.environ, {"LOGGING_LEVEL": "INVALID_LEVEL"})
    def test_read_invalid_logging_environment_variable_defaults_to_info(self):
        config = settings.Config()

        self.assertEqual("INFO", config.LOGGING_LEVEL)
