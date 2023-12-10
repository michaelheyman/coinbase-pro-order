from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pair:
    base_currency: str
    quote_currency: str
