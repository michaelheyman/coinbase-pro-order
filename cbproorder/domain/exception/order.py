from cbproorder.domain.value_object.orders import OrderType


class UnsupportedOrderType(Exception):
    """
    Exception raised when an unsupported order type is used.

    Attributes:
        order_type (str): The unsupported order type.
    """

    def __init__(self, order_type: OrderType):
        """
        Constructs an instance of the UnsupportedOrderType exception.

        Args:
            order_type (OrderType): The unsupported order type.
        """
        self.order_type = order_type
        super().__init__(f"Unsupported order type: {str(self.order_type)}")
