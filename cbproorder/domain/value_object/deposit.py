import dataclasses

from pydantic import Field, TypeAdapter
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Deposit:
    """
    A class to represent a deposit.
    """

    amount: float = Field(..., description="The amount to deposit.")
    currency: str = Field(..., description="The currency of the deposit.")

    @classmethod
    def from_dict(cls, deposit_dict: dict) -> "Deposit":
        """
        Create a Deposit instance from a dictionary.

        Args:
            deposit_dict (dict): The dictionary with the deposit data. It should have 'amount' and 'currency' keys.

        Returns:
            Deposit: The created Deposit instance.

        Raises:
            ValidationError: If the data dictionary doesn't have the required keys or the values are not of the expected type.
        """
        deposit = {
            "amount": deposit_dict["amount"],
            "currency": deposit_dict["currency"],
        }
        return TypeAdapter(cls).validate_python(deposit)


@dataclasses.dataclass(frozen=True, slots=True)
class DepositResult:
    """
    A data class that represents the result of a deposit operation.

    Attributes:
        status (str): The status of the deposit.
        currency (str): The currency of the deposit.
        amount (float): The amount of the deposit. Defaults to None.
        fee (float): The fee for the deposit. Defaults to None.
    """

    status: str
    currency: str
    amount: float = None
    fee: float = None

    @classmethod
    def from_deposit_dict(cls, deposit: dict) -> "DepositResult":
        """
        Create a DepositResult instance from a dictionary.

        Args:
            deposit (dict): A dictionary with keys 'status', 'currency', 'amount', and 'fee'.

        Returns:
            DepositResult: A DepositResult instance with the data from the dictionary.
        """
        amount = deposit.get("amount", {}).get("amount")
        fee = deposit.get("fee", {}).get("amount")
        return cls(
            status=deposit["status"],
            currency=deposit["amount"]["currency"],
            amount=float(amount) if amount else None,
            fee=float(fee) if fee else None,
        )
