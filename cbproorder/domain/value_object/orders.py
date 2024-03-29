import dataclasses
from enum import Enum

from pydantic import Field, TypeAdapter
from pydantic.dataclasses import dataclass

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
    """

    pair: Pair = Field(..., description="The currency pair for the order.")
    quote_size: float = Field(
        ...,
        ge=10.0,
        description="The size of the order in quote currency.",
    )
    side: OrderSide = Field(..., description="The side of the order (buy or sell).")
    type: OrderType = Field(
        ...,
        description="The type of the order (limit, market, or stop).",
    )

    @classmethod
    def from_dict(cls, order_dict: dict) -> "Order":
        """
        Create an Order from a dict.

        Args:
            order_dict (dict): A dict representing an order.

        Returns:
            Order: The Order created from the dict.
        """
        order = {
            "pair": Pair.from_string(order_dict["product_id"]),
            "quote_size": order_dict["price"],
            "side": OrderSide.BUY,
            "type": OrderType.MARKET,
        }
        return TypeAdapter(cls).validate_python(order)


@dataclasses.dataclass(frozen=True, slots=True)
class OrderResult:
    """
    A class to represent the result of an order operation.

    This class encapsulates whether the operation was successful, the original order, the ID of the order (if it was created), the product ID associated with the order, the quote size of the order, the base size of the order, the side of the order, and any error message (if the operation failed).

    Attributes:
        success (bool): Whether the operation was successful.
        order_id (str | None): The ID of the order, if it was created.
        product_id (str | None): The product ID associated with the order.
        quote_size (str | None): The quote size of the order.
        base_size (str | None): The base size of the order.
        side (str | None): The side of the order.
        error (str | None): Any error code, if the operation failed.
        error_message (str | None): Any error message, if the operation failed.
        error_details (str | None): Any error details, if the operation failed.
    """

    success: bool = Field(False, description="Whether the operation was successful.")
    # Success fields
    order_id: str | None = None
    product_id: str | None = None
    quote_size: str | None = None
    base_size: str | None = None
    side: str | None = None
    # Error fields
    error: str | None = None
    error_message: str | None = None
    error_details: str | None = None
