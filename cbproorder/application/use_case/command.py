from dataclasses import dataclass

from cbproorder.domain.deposit_service import DepositService
from cbproorder.domain.factories.notification_message import NotificationMessageFactory
from cbproorder.domain.notification_service import NotificationService
from cbproorder.domain.order_service import OrderService
from cbproorder.domain.value_object.deposit import DepositResult
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

        message = NotificationMessageFactory().create_message(
            type="order_created",
            quote_size=self.order.quote_size,
            pair=self.order.pair,
        )
        self.notification_service.send_notification(message=message)
        return created_order


@dataclass(frozen=True, slots=True)
class SubmitDepositCommand:
    """
    A command to submit a deposit.

    Attributes:
        amount (float): The amount to deposit.
        currency (str): The currency of the deposit.
    """

    amount: float
    currency: str


class SubmitDepositCommandUseCase:
    """
    A use case for submitting a deposit.
    """

    def __init__(
        self,
        deposit_service: DepositService,
        notification_service: NotificationService,
    ):
        """
        Initialize the SubmitDepositCommandUseCase with the given deposit and notification services.

        Args:
            deposit_service (DepositService): The service to use for depositing.
            notification_service (NotificationService): The service to use for sending notifications.
        """
        self.deposit_service = deposit_service
        self.notification_service = notification_service

    def deposit_usd(self, command: SubmitDepositCommand) -> DepositResult:
        """
        Deposit USD using the given command.

        Args:
            command (SubmitDepositCommand): The command to use for the deposit.

        Returns:
            DepositResult: The result of the deposit operation.
        """
        deposit_result = self.deposit_service.deposit_usd(command.amount)
        message = NotificationMessageFactory().create_message(
            type="deposit_completed",
            amount=deposit_result.amount,
            currency=deposit_result.currency,
        )
        self.notification_service.send_notification(message=message)
        return deposit_result
