import os
import uuid
from typing import Any

from cbproorder.domain.exception.order import UnsupportedOrderType
from cbproorder.domain.order_service import OrderService
from cbproorder.domain.value_object.orders import Order, OrderResult, OrderType
from cbproorder.infrastructure.logger import get_logger

logger = get_logger(__name__)


class CoinbaseAdvancedService(OrderService):
    """
    A class to represent the Coinbase Advanced Service.

    This class is a concrete implementation of the OrderServiceInterface for the Coinbase
    Developer Platform.
    """

    def __init__(self, api_key_name: str, private_key: str) -> None:
        """
        Constructs an instance of the CoinbaseAdvancedService.

        Args:
            api_key_name (str): The API key for the Coinbase Advanced Trade API.
            private_key (str): The secret key for the Coinbase Advanced Trade API.

        The service uses the environment variable COINBASE_API_BASE_URL to
        override the base URL for testing purposes.
        If COINBASE_API_BASE_URL is set, the service will use this as the
        base URL, otherwise, it will use the default base URL.
        """
        from coinbase.rest import RESTClient

        if os.getenv("COINBASE_API_BASE_URL"):
            self.client = RESTClient(
                api_key=api_key_name,
                api_secret=private_key,
                base_url=os.getenv("COINBASE_API_BASE_URL"),
            )
            return

        self.client = RESTClient(
            api_key=api_key_name,
            api_secret=private_key,
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
        created_order = self.client.market_order_buy(
            client_order_id=client_order_id,
            product_id=product_id,
            quote_size=str(order.quote_size),
        )
        logger.info("Created by market order", extra={"order": created_order})

        return self._order_result_from_coinbase_advanced_order(
            coinbase_order_response=created_order,
            product_id=product_id,
        )

    def _order_result_from_coinbase_advanced_order(
        self,
        coinbase_order_response: dict[str, Any],
        product_id: str,
    ) -> OrderResult:
        """
        Create an OrderResult object from a the response of the retailbrokerageapi_postorder endpoint.

        Documentation on this endpoint can be found here:

        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_postorder

        Args:
            order (dict[str, Any]): The response order object to convert.

        Returns:
            OrderResult: The converted OrderResult object.
        """
        success = coinbase_order_response.get("success", False)

        if coinbase_order_response.get("error_response"):
            return OrderResult(
                success=success,
                order_id=coinbase_order_response.get("order_id"),
                product_id=product_id,
                error=coinbase_order_response.get("error_response", {}).get("error"),
                error_message=coinbase_order_response.get("error_response", {}).get(
                    "message"
                ),
                error_details=coinbase_order_response.get("error_response", {}).get(
                    "error_details"
                ),
            )

        return OrderResult(
            success=success,
            order_id=coinbase_order_response.get("order_id"),
            product_id=product_id,
            quote_size=coinbase_order_response.get("order_configuration", {})
            .get("market_market_ioc", {})
            .get("quote_size"),
            base_size=coinbase_order_response.get("order_configuration", {})
            .get("market_market_ioc", {})
            .get("base_size"),
            side=coinbase_order_response.get("success_response", {}).get("side"),
        )
