from abc import ABC, abstractmethod

from cbproorder.domain.value_object.deposit import DepositResult


class DepositService(ABC):
    """
    Get the ID of the primary ACH payment method.

    Returns:
        str | None: The ID of the primary ACH payment method if it exists, otherwise None.
    """

    @abstractmethod
    def deposit_usd(self, amount: float) -> DepositResult:
        """
        Deposit the given amount of USD.

        This is an abstract method that must be implemented in subclasses.

        Args:
            amount (float): The amount of USD to deposit.

        Returns:
            DepositResult: The result of the deposit operation.
        """
        pass  # pragma: no cover
