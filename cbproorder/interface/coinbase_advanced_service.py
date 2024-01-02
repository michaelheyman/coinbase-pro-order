import os
import uuid

from coinbaseadvanced import client
from coinbaseadvanced.models.orders import Order as CoinbaseAdvancedOrder

from cbproorder.domain.exception.order import UnsupportedOrderType
from cbproorder.domain.order_service import OrderService
from cbproorder.domain.value_object.orders import Order, OrderResult, OrderType
from cbproorder.infrastructure.logger import get_logger

logger = get_logger(__name__)


class CoinbaseAdvancedService(OrderService):
    """
    A class to represent the Coinbase Advanced Service.

    This class is a concrete implementation of the OrderServiceInterface for the Coinbase Advanced API.
    """

    def __init__(self, api_key: str, secret_key: str) -> None:
        """
        Constructs an instance of the CoinbaseAdvancedService.

        Args:
            api_key (str): The API key for the Coinbase Advanced Trade API.
            secret_key (str): The secret key for the Coinbase Advanced Trade API.

        The service uses the environment variable COINBASE_API_BASE_URL to
        override the base URL for testing purposes.
        If COINBASE_API_BASE_URL is set, the service will use this as the
        base URL, otherwise, it will use the default base URL.
        """
        if os.getenv("COINBASE_API_BASE_URL"):
            self.client = client.CoinbaseAdvancedTradeAPIClient(
                api_key=api_key,
                secret_key=secret_key,
                base_url=os.getenv("COINBASE_API_BASE_URL"),
            )
            return

        self.client = client.CoinbaseAdvancedTradeAPIClient(
            api_key=api_key,
            secret_key=secret_key,
        )

    def create_market_buy_order(self, order: Order) -> OrderResult:
        """
        Create a buy type market order.

        Args:
            order (Order): The order to create a market buy order.

        Raises:
            UnsupportedOrderType: If the order type is not MARKET.

        Returns:
            OrderResult: The result of the order operation, encapsulating whether the operation was successful, the original order, and any error message (if the operation failed).
        """
        if order.type != OrderType.MARKET:
            raise UnsupportedOrderType(order.type)

        product_id = f"{order.pair.base_currency}-{order.pair.quote_currency}"
        client_order_id = str(uuid.uuid4())
        created_order = self.client.create_buy_market_order(
            client_order_id=client_order_id,
            product_id=product_id,
            quote_size=order.quote_size,
        )
        logger.info("Created by market order", extra={"order": created_order})

        return self._order_result_from_coinbase_advanced_order(
            coinbase_order_response=created_order,
        )

    def _order_result_from_coinbase_advanced_order(
        self,
        coinbase_order_response: CoinbaseAdvancedOrder,
    ) -> OrderResult:
        """
        Create an OrderResult object from a CoinbaseAdvancedOrder object.

        The CoinbaseAdvancedOrder object is returned from the Coinbase Advanced
        Trade API, and its documentation can be found here:

        https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder

        Args:
            order (CoinbaseAdvancedOrder): The CoinbaseAdvancedOrder object to convert.

        Returns:
            OrderResult: The converted OrderResult object.
        """
        success = (
            True
            if coinbase_order_response.order_id and coinbase_order_response.side
            else False
        )

        if coinbase_order_response.order_error:
            return OrderResult(
                success=False,
                order_id=coinbase_order_response.order_id,
                product_id=coinbase_order_response.product_id,
                error=coinbase_order_response.order_error.error,
                error_message=coinbase_order_response.order_error.message,
                error_details=coinbase_order_response.order_error.error_details,
            )

        return OrderResult(
            success=success,
            order_id=coinbase_order_response.order_id,
            product_id=coinbase_order_response.product_id,
            quote_size=coinbase_order_response.order_configuration.market_market_ioc.quote_size,
            base_size=coinbase_order_response.order_configuration.market_market_ioc.base_size,
            side=coinbase_order_response.side,
        )
