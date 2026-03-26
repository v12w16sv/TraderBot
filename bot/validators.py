"""
Input validation utilities
"""
from typing import Tuple, Optional


class OrderValidator:
    """Validate order inputs"""
    
    VALID_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'XRPUSDT', 'SOLUSDT', 'LINKUSDT']
    VALID_SIDES = ['BUY', 'SELL']
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT']
    
    @classmethod
    def validate_symbol(cls, symbol: str) -> Tuple[bool, str]:
        """
        Validate trading symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            (is_valid, error_message)
        """
        if not symbol:
            return False, "Symbol cannot be empty"
        
        symbol = symbol.upper()
        if symbol not in cls.VALID_SYMBOLS:
            return False, f"Invalid symbol. Must be one of: {', '.join(cls.VALID_SYMBOLS)}"
        
        return True, ""
    
    @classmethod
    def validate_side(cls, side: str) -> Tuple[bool, str]:
        """
        Validate order side
        
        Args:
            side: BUY or SELL
            
        Returns:
            (is_valid, error_message)
        """
        if not side:
            return False, "Side cannot be empty"
        
        side = side.upper()
        if side not in cls.VALID_SIDES:
            return False, f"Invalid side. Must be BUY or SELL"
        
        return True, ""
    
    @classmethod
    def validate_order_type(cls, order_type: str) -> Tuple[bool, str]:
        """
        Validate order type
        
        Args:
            order_type: MARKET or LIMIT
            
        Returns:
            (is_valid, error_message)
        """
        if not order_type:
            return False, "Order type cannot be empty"
        
        order_type = order_type.upper()
        if order_type not in cls.VALID_ORDER_TYPES:
            return False, f"Invalid order type. Must be MARKET or LIMIT"
        
        return True, ""
    
    @classmethod
    def validate_quantity(cls, quantity: float, symbol: str = "BTCUSDT") -> Tuple[bool, str]:
        """
        Validate order quantity
        
        Args:
            quantity: Order quantity
            symbol: Trading symbol (for future min/max validation)
            
        Returns:
            (is_valid, error_message)
        """
        if quantity is None:
            return False, "Quantity cannot be empty"
        
        try:
            quantity = float(quantity)
        except (ValueError, TypeError):
            return False, "Quantity must be a number"
        
        if quantity <= 0:
            return False, "Quantity must be greater than 0"
        
        # Basic min quantity check (BTCUSDT min is 0.001)
        if quantity < 0.001:
            return False, "Quantity too small. Minimum is 0.001"
        
        if quantity > 1000:
            return False, "Quantity too large. Maximum is 1000"
        
        return True, ""
    
    @classmethod
    def validate_price(cls, price: float, symbol: str = "BTCUSDT") -> Tuple[bool, str]:
        """
        Validate order price
        
        Args:
            price: Order price
            symbol: Trading symbol
            
        Returns:
            (is_valid, error_message)
        """
        if price is None:
            return False, "Price is required for LIMIT orders"
        
        try:
            price = float(price)
        except (ValueError, TypeError):
            return False, "Price must be a number"
        
        if price <= 0:
            return False, "Price must be greater than 0"
        
        return True, ""
    
    @classmethod
    def validate_all(cls, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Tuple[bool, str]:
        """
        Validate all order parameters
        
        Returns:
            (is_valid, error_message)
        """
        # Validate symbol
        valid, msg = cls.validate_symbol(symbol)
        if not valid:
            return False, msg
        
        # Validate side
        valid, msg = cls.validate_side(side)
        if not valid:
            return False, msg
        
        # Validate order type
        valid, msg = cls.validate_order_type(order_type)
        if not valid:
            return False, msg
        
        # Validate quantity
        valid, msg = cls.validate_quantity(quantity, symbol)
        if not valid:
            return False, msg
        
        # Validate price for LIMIT orders
        if order_type.upper() == 'LIMIT':
            valid, msg = cls.validate_price(price, symbol)
            if not valid:
                return False, msg
        
        return True, "All validations passed"