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

    def __init__(self, api_key: str, secret_key: str):
        """
        Constructs an instance of the CoinbaseDepositService.

        Args:
            api_key (str): The API key for the Coinbase API.
            secret_key (str): The secret key for the Coinbase API.
        """
        from coinbase.wallet.client import Client

        if os.getenv("COINBASE_API_BASE_URL"):
            self.client = Client(
                api_key=api_key,
                api_secret=secret_key,
                base_api_uri=os.getenv("COINBASE_API_BASE_URL"),
            )
            return

        self.client = Client(
            api_key=api_key,
            api_secret=secret_key,
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
        accounts = self.client.get_accounts()

        if not accounts or not accounts.get("data"):
            return None

        for account in accounts["data"]:
            # There should only be one account with balance.currency of USD
            if account.get("balance", {}).get("currency") == self._USD_CURRENCY:
                return account["id"]
        return None

    def get_ach_payment_method_id(self) -> str | None:
        """
        Get the ID of the primary ACH payment method.

        Returns:
            str | None: The ID of the primary ACH payment method if it exists, otherwise None.
        """
        payment_methods = self.client.get_payment_methods()

        if not payment_methods or not payment_methods.get("data"):
            return None

        for payment_method in payment_methods["data"]:
            # There should only be one primary_buy payment method
            if payment_method["primary_buy"]:
                return payment_method["id"]
        return None
