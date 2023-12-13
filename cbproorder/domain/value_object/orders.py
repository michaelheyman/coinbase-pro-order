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


@dataclass
class OrderResult:
    """
    A class to represent the result of an order operation.

    This class encapsulates whether the operation was successful, the original order, the ID of the order (if it was created), the status of the order, and any error message (if the operation failed).

    Attributes:
        success (bool): Whether the operation was successful.
        order (Order): The original order.
        order_id (str, optional): The ID of the order, if it was created. Defaults to None.
        status (str, optional): The status of the order. Defaults to None.
        error_message (str, optional): Any error message, if the operation failed. Defaults to None.
    """

    success: bool
    order: Order
    order_id: str = None
    status: str = None
    error_message: str = None
