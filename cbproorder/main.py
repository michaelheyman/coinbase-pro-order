"""Application script."""
import cbpro

from cbproorder import settings
from cbproorder.logger import logger


def start():
    """Authenticate with Coinbase and execute orders."""
    try:
        coinbase = settings.CoinbaseConfig()
    except EnvironmentError:
        logger.error("There was an error loading your Coinbase credentials", exc_info=1)
        return

    config = settings.Config()
    auth_client = cbpro.AuthenticatedClient(
        key=coinbase.API_KEY,
        b64secret=coinbase.API_SECRET,
        passphrase=coinbase.API_PASSPHRASE,
        api_url=config.SANDBOX_API_URL,
    )
    currencies = auth_client.get_currencies()
    logger.info(currencies)
    logger.info("done")
