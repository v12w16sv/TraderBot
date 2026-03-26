"""
Binance Futures Testnet client wrapper - MOCK IMPLEMENTATION
Simulates API responses for testing and demonstration
"""
import time
import random
from typing import Dict, Optional
from datetime import datetime

from .logging_config import logger


class BinanceFuturesClient:
    """Mock Binance Futures API client for testing"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True, mock_mode: bool = True):
        """
        Initialize mock Binance Futures client
        
        Args:
            api_key: Binance API key (can be dummy in mock mode)
            api_secret: Binance API secret (can be dummy in mock mode)
            testnet: Use testnet endpoint (just for logging)
            mock_mode: If True, returns mock responses without real API calls
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.mock_mode = mock_mode
        self.order_counter = 1000000  # Start order IDs from 1 million
        
        if mock_mode:
            logger.info("RUNNING IN MOCK MODE - Simulating API responses (no real API calls)")
            logger.info("   Base URL would be: https://testnet.binancefuture.com")
        else:
            logger.info(f"Initialized Binance Futures client with base URL: https://testnet.binancefuture.com")
    
    def _generate_mock_order_id(self) -> int:
        """Generate a unique mock order ID"""
        self.order_counter += random.randint(1, 100)
        return self.order_counter
    
    def get_account_info(self) -> Dict:
        """Mock account information"""
        if self.mock_mode:
            return {
                'accountAlias': 'TestAccount',
                'assets': [
                    {'asset': 'USDT', 'walletBalance': '10000.00', 'unrealizedProfit': '0.00'},
                    {'asset': 'BTC', 'walletBalance': '0.10', 'unrealizedProfit': '0.00'}
                ],
                'canDeposit': True,
                'canTrade': True,
                'canWithdraw': True
            }
        return {}
    
    def get_symbol_price(self, symbol: str) -> float:
        """Mock current price"""
        if self.mock_mode:
            # Generate realistic mock prices
            prices = {
                'BTCUSDT': 49850.50,
                'ETHUSDT': 2850.75,
                'BNBUSDT': 520.30,
                'ADAUSDT': 0.45,
                'DOGEUSDT': 0.12,
                'XRPUSDT': 0.55,
                'SOLUSDT': 105.20,
                'LINKUSDT': 18.75
            }
            price = prices.get(symbol.upper(), 50000.00)
            logger.debug(f"Mock price for {symbol}: {price}")
            return price
        return 0.0
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict:
        """
        Place a mock order - returns realistic simulated response
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Price for LIMIT orders
            
        Returns:
            Mock order response
        """
        if not self.mock_mode:
            # Real API implementation would go here
            raise NotImplementedError("Real API not implemented - use mock_mode=True")
        
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()
        
        # Generate mock order details
        order_id = self._generate_mock_order_id()
        current_price = self.get_symbol_price(symbol)
        
        # Calculate mock values
        if order_type == 'MARKET':
            exec_price = current_price
            status = 'FILLED'
            executed_qty = quantity
            avg_price = exec_price
        else:  # LIMIT
            exec_price = price if price else current_price
            status = 'NEW'  # Limit orders start as 'NEW', not filled
            executed_qty = 0
            avg_price = None
        
        # Create mock response
        response = {
            'orderId': order_id,
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': str(quantity),
            'price': str(price) if price else '0',
            'status': status,
            'executedQty': str(executed_qty),
            'origQty': str(quantity),
            'time': int(time.time() * 1000),
            'updateTime': int(time.time() * 1000),
            'clientOrderId': f"mock_order_{order_id}",
            'workingTime': int(time.time() * 1000)
        }
        
        if avg_price:
            response['avgPrice'] = str(avg_price)
        
        # Log the mock order
        logger.info(f"MOCK ORDER: {order_type} {side} {quantity} {symbol}" + 
                   (f" @ {price}" if price else f" @ market ({current_price})") +
                   f" -> Order ID: {order_id}, Status: {status}")
        
        return response
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Mock cancel order"""
        if self.mock_mode:
            return {
                'orderId': order_id,
                'symbol': symbol,
                'status': 'CANCELED',
                'clientOrderId': f"mock_order_{order_id}",
                'time': int(time.time() * 1000)
            }
        return {}
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """Mock get order status"""
        if self.mock_mode:
            return {
                'orderId': order_id,
                'symbol': symbol,
                'status': 'FILLED',
                'executedQty': '0.01',
                'price': '50000.00'
            }
        return {}