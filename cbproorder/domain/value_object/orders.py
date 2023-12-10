from enum import Enum
from dataclasses import dataclass

from cbproorder.domain.value_object.pair import Pair


class OrderSide(Enum):
    """
    Enum representing supported directions of orders.
    """

    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """
    Enum representing supported order types.
    """

    LIMIT = "limit"
    MARKET = "market"
    STOP = "stop"


@dataclass(frozen=True, slots=True)
class Order:
    pair: Pair
    quote_size: float
    side: OrderSide
    type: OrderType
