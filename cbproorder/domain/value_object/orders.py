from dataclasses import dataclass
from enum import Enum

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
    """
    A class to represent an order.

    Attributes:
        pair (Pair): The currency pair for the order.
        quote_size (float): The size of the order in quote currency.
        side (OrderSide): The side of the order (buy or sell).
        type (OrderType): The type of the order (limit, market, or stop).
    """

    pair: Pair
    quote_size: float
    side: OrderSide
    type: OrderType
