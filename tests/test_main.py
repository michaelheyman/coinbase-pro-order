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
