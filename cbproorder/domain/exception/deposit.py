class DepositAccountNotFound(Exception):
    """
    Exception raised when a deposit account is not found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self) -> None:
        """
        Initialize the DepositAccountNotFound exception with a default message.
        """
        super().__init__("Deposit account not found")


class DepositPaymentMethodNotFound(Exception):
    """
    Exception raised when a deposit payment method is not found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self) -> None:
        """
        Initialize the DepositPaymentMethodNotFound exception with a default message.
        """
        super().__init__("Deposit payment method not found")
