from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pair:
    """
    A class to represent a currency pair.

    Attributes:
        base_currency (str): The base currency of the pair.
        quote_currency (str): The quote currency of the pair.
    """

    base_currency: str
    quote_currency: str

    @classmethod
    def from_string(cls, pair_string: str):
        """
        Create a Pair object from a string.

        Args:
            pair_string (str): A string representation of a currency pair, in the format 'BASE-QUOTE'.

        Returns:
            Pair: A Pair object representing the currency pair.
        """
        base, quote = pair_string.split("-")
        return cls(base, quote)

    def __str__(self):
        """
        Create a string representation of the Pair object.

        Returns:
            str: A string representation of the Pair object, in the format 'BASE-QUOTE'.
        """
        return f"{self.base_currency}-{self.quote_currency}"
