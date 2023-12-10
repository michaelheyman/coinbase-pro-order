from abc import ABC, abstractmethod

from cbproorder.domain.value_object.orders import Order


class OrderServiceInterface(ABC):
    @abstractmethod
    def create_market_buy_order(self, order: Order):
        pass
