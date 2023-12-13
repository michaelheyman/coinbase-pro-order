from cbproorder.application.notification_service import NotificationService
from cbproorder.application.order_service import OrderService
from cbproorder.domain.value_object.orders import (
    Order,
    OrderResult,
    OrderSide,
    OrderType,
)
from cbproorder.domain.value_object.pair import Pair


class SubmitMarketBuyOrderCommand:
    """
    A class to represent a command to submit a market buy order.
    """

    def __init__(self, product_id: str, funds: float):
        """
        Constructs an instance of the SubmitMarketBuyOrderCommand.

        Args:
            product_id (str): The product ID of the order.
            funds (float): The size of the order in quote currency.
        """
        self.product_id = product_id
        self.funds = funds


class SubmitMarketBuyOrderCommandUseCase:
    """
    A class to represent a use case for submitting a market buy order.

    Attributes:
        order_service (OrderService): The order service to use for submitting the order.
    """

    def __init__(
        self,
        order_service: OrderService,
        notification_service: NotificationService,
    ):
        """
        Constructs an instance of the SubmitMarketBuyOrderCommandUseCase.

        Args:
            notification_service (NotificationService): The notification service to use for submitting notifications.
            order_service (OrderService): The order service to use for submitting the order.
        """
        self.notification_service = notification_service
        self.order_service = order_service

    def create_market_buy_order(
        self,
        command: SubmitMarketBuyOrderCommand,
    ) -> OrderResult:
        """
        Create a buy type market order.

        Args:
            command (SubmitMarketBuyOrderCommand): The command to create a market buy order.

        Returns:
            OrderResponse: The response from the order service.
        """
        self.order: Order = Order(
            pair=Pair.from_string(command.product_id),
            quote_size=command.funds,
            side=OrderSide.BUY,
            type=OrderType.MARKET,
        )
        created_order = self.order_service.create_market_buy_order(self.order)

        # TODO: modify notification based on the result of creating an order
        self.notification_service.send_notification(
            title="Order Created",
            message=f"Order created for {self.order.pair} at {self.order.quote_size}",
        )
        return created_order
