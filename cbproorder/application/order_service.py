from abc import ABC, abstractmethod

from cbproorder.domain.value_object.orders import Order


class OrderServiceInterface(ABC):
    """
    A class to represent the interface for an order service.

    This class is meant to be subclassed by concrete implementations of an order service.
    """

    @abstractmethod
    def create_market_buy_order(self, order: Order):
        """
        Create a market buy order.

        This method should be implemented by subclasses to create a market buy order using the specific logic of the order service.

        Args:
            order (Order): The order to create.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass
