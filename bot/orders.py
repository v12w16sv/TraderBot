"""
Order placement logic
"""
from typing import Dict, Optional
from .client import BinanceFuturesClient
from .validators import OrderValidator
from .logging_config import logger


class OrderManager:
    """Manage order placement and execution"""
    
    def __init__(self, client: BinanceFuturesClient):
        """
        Initialize order manager
        
        Args:
            client: Binance Futures client
        """
        self.client = client
        logger.info("Order manager initialized")
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict:
        """
        Place an order with validation
        
        Args:
            symbol: Trading symbol
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Price for LIMIT orders
            
        Returns:
            Order response
        """
        # Validate inputs
        valid, message = OrderValidator.validate_all(symbol, side, order_type, quantity, price)
        if not valid:
            logger.error(f"Validation failed: {message}")
            raise ValueError(f"Validation error: {message}")
        
        # Convert to uppercase for API
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()
        
        # Get current price for MARKET orders (for logging)
        if order_type == 'MARKET':
            current_price = self.client.get_symbol_price(symbol)
            logger.info(f"Current market price for {symbol}: {current_price}")
        
        # Place order
        try:
            result = self.client.place_order(symbol, side, order_type, quantity, price)
            
            # Log order details
            logger.info(f"Order placed - Order ID: {result.get('orderId')}, "
                       f"Status: {result.get('status')}, "
                       f"Executed Qty: {result.get('executedQty', 0)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            raise
    
    def format_order_output(self, order_response: Dict, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> str:
        """
        Format order response for display
        
        Returns:
            Formatted output string
        """
        output = []
        output.append("=" * 50)
        output.append("ORDER REQUEST SUMMARY")
        output.append("=" * 50)
        output.append(f"Symbol: {symbol}")
        output.append(f"Side: {side}")
        output.append(f"Type: {order_type}")
        output.append(f"Quantity: {quantity}")
        if price:
            output.append(f"Price: {price}")
        output.append("")
        output.append("ORDER RESPONSE")
        output.append("-" * 30)
        output.append(f"Order ID: {order_response.get('orderId')}")
        output.append(f"Status: {order_response.get('status')}")
        output.append(f"Executed Quantity: {order_response.get('executedQty', '0')}")
        
        if 'avgPrice' in order_response and order_response['avgPrice']:
            output.append(f"Average Price: {order_response['avgPrice']}")
        elif 'price' in order_response and order_response['price']:
            output.append(f"Price: {order_response['price']}")
        
        output.append(f"Client Order ID: {order_response.get('clientOrderId', 'N/A')}")
        output.append("=" * 50)
        
        if order_response.get('status') == 'FILLED':
            output.append("SUCCESS: Order filled successfully!")
        elif order_response.get('status') == 'NEW':
            output.append("SUCCESS: Order placed successfully (pending fill)!")
        else:
            output.append(f"Order status: {order_response.get('status')}")
        
        return "\n".join(output)