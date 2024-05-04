import os

from cbproorder.domain.deposit_service import DepositService
from cbproorder.domain.exception.deposit import (
    DepositAccountNotFound,
    DepositPaymentMethodNotFound,
)
from cbproorder.domain.value_object.deposit import DepositResult
from cbproorder.infrastructure.logger import get_logger

logger = get_logger(__name__)


class CoinbaseDepositService(DepositService):
    """
    A service class for making deposits to a Coinbase account.

    Attributes:
        client: A Coinbase client instance for making API calls.
    """

    _USD_CURRENCY = "USD"

    def __init__(
        self, api_key: str, secret_key: str, api_key_name: str, private_key: str
    ):
        """
        Constructs an instance of the CoinbaseDepositService.

        This service uses both the Coinbase REST and Wallet clients to make API
        calls. The former is the most recent official Coinbase client, and it
        is used for retrieving the deposit account and ACH payment method IDs.
        The latter is a 3rd party client that is used for making the deposit
        itself, since there is no deposit support in the official client.

        In other words, the REST client uses the Advanced Trade API, while the
        Wallet client uses the v2 API, which has deprecated endpoints, but is
        the only one that supports deposits at the moment.

        Args:
            api_key (str): The API key for the Coinbase Wallet API.
            secret_key (str): The secret key for the Coinbase Wallet API.
            api_key_name (str): The API key for the Coinbase Advanced Trade API.
            private_key (str): The secret key for the Coinbase Advanced Trade API.
        """
        from coinbase.rest import RESTClient
        from coinbase.wallet.client import Client

        if os.getenv("COINBASE_API_BASE_URL"):
            logger.info(
                "Overriding Coinbase API base URL",
                extra={"url": os.getenv("COINBASE_API_BASE_URL")},
            )
            self.client = Client(
                api_key=api_key,
                api_secret=secret_key,
                base_api_uri=os.getenv("COINBASE_API_BASE_URL"),
            )
            self.advanced_client = RESTClient(
                api_key=api_key_name,
                api_secret=private_key,
                base_api_uri=os.getenv("COINBASE_API_BASE_URL"),
            )
            return

        self.client = Client(
            api_key=api_key,
            api_secret=secret_key,
        )
        self.advanced_client = RESTClient(
            api_key=api_key_name,
            api_secret=private_key,
        )

    def deposit_usd(self, amount: float) -> DepositResult:
        """
        Deposit the given amount of USD to the account.

        See https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-deposits.

        Args:
            amount (float): The amount of USD to deposit.

        Raises:
            Exception: If no deposit account or ACH payment method is found.

        Returns:
            DepositResult: The result of the deposit operation.
        """
        deposit_account_id = self.get_deposit_account_id()
        if deposit_account_id is None:
            raise DepositAccountNotFound()

        ach_payment_method_id = self.get_ach_payment_method_id()
        if ach_payment_method_id is None:
            raise DepositPaymentMethodNotFound()

        logger.info(
            "Depositing USD to Coinbase account",
            extra={
                "account_id": deposit_account_id,
                "payment_method": ach_payment_method_id,
                "amount": amount,
            },
        )
        deposit = self.client.deposit(
            account_id=deposit_account_id,
            payment_method=ach_payment_method_id,
            amount=str(amount),
            currency=self._USD_CURRENCY,
        )
        logger.info("Deposit created", extra={"deposit": deposit})
        result = DepositResult.from_deposit_dict(deposit)
        logger.info("Deposit result", extra={"result": result})
        return result

    def get_deposit_account_id(self) -> str | None:
        """
        Get the ID of the deposit account.

        Returns:
            str | None: The ID of the deposit account if it exists, otherwise None.
        """
        accounts = self.advanced_client.get_accounts()

        if not accounts or not accounts.get("accounts"):
            return None

        for account in accounts["accounts"]:
            if account.get("type") == "ACCOUNT_TYPE_FIAT":
                return account["uuid"]
        return None

    def get_ach_payment_method_id(self) -> str | None:
        """
        Get the ID of the primary ACH payment method.

        Returns:
            str | None: The ID of the primary ACH payment method if it exists, otherwise None.
        """
        payment_methods = self.advanced_client.list_payment_methods()

        if not payment_methods or not payment_methods.get("payment_methods"):
            return None

        logger.debug(
            "Coinbase ACH payment methods",
            extra={"payment_methods": payment_methods},
        )
        for payment_method in payment_methods["payment_methods"]:
            # The payment method must be of type ACH and allow deposits
            if (
                payment_method["type"].lower() == "ach"
                and payment_method["allow_deposit"]
            ):
                logger.debug(
                    "Payment method selected",
                    extra={"payment_method": payment_method},
                )
                return payment_method["id"]
        return None
