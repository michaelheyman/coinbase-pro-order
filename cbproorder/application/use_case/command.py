from cbproorder.application.order_service import OrderService
from cbproorder.domain.value_object.orders import Order, OrderSide, OrderType
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


class OrderResponse:
    """
    A class to represent the response from submitting an order.

    Attributes:
        id (str): The ID of the order.
        product_id (str): The product ID of the order.
        side (str): The side of the order (buy or sell).
        type (str): The type of the order (limit, market, or stop).
        funds (float): The size of the order in quote currency.
    """

    def __init__(self, order: Order):
        """
        Constructs an instance of the OrderResponse.

        Args:
            order (Order): The order that was submitted.
        """
        self.id = order.id
        self.product_id = str(order.pair)
        self.side = order.side
        self.type = order.type
        self.funds = order.quote_size


class SubmitMarketBuyOrderCommandUseCase:
    """
    A class to represent a use case for submitting a market buy order.

    Attributes:
        order_service (OrderService): The order service to use for submitting the order.
    """

    def __init__(self, order_service: OrderService):
        """
        Constructs an instance of the SubmitMarketBuyOrderCommandUseCase.

        Args:
            order_service (OrderService): The order service to use for submitting the order.
        """
        self.order_service = order_service

    def create_market_buy_order(
        self,
        command: SubmitMarketBuyOrderCommand,
    ) -> OrderResponse:
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
        return OrderResponse(created_order)
