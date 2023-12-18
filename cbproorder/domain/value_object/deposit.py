from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
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
    def from_deposit_dict(cls, deposit: dict):
        """
        Create a DepositResult instance from a dictionary.

        Args:
            deposit (dict): A dictionary with keys 'status', 'currency', 'amount', and 'fee'.

        Returns:
            DepositResult: A DepositResult instance with the data from the dictionary.
        """
        data = deposit.get("data", {})
        amount = data.get("amount", {}).get("amount")
        fee = data.get("fee", {}).get("amount")
        return cls(
            status=data.get("status"),
            currency=data.get("amount", {}).get("currency"),
            amount=float(amount) if amount else None,
            fee=float(fee) if fee else None,
        )
