#!/usr/bin/env python3
"""
Trading Bot CLI - Mock Implementation
Simulates Binance Futures Testnet trading
"""
import os
import sys
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.logging_config import logger


# Load environment variables
load_dotenv()

# Configuration - Mock mode is ON by default
API_KEY = os.getenv('BINANCE_API_KEY', 'mock_api_key_12345')
API_SECRET = os.getenv('BINANCE_API_SECRET', 'mock_secret_key_67890')
TESTNET = os.getenv('TESTNET', 'true').lower() == 'true'
MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'


def validate_environment():
    """Check if API credentials are set (mock mode accepts any)"""
    if not MOCK_MODE:
        if not API_KEY or not API_SECRET or API_KEY == 'your_api_key_here':
            logger.error("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET")
            print("\nERROR: API credentials not configured!")
            print("For mock mode, this is optional. Set MOCK_MODE=true in .env")
            print("\nOr create a .env file with:")
            print("BINANCE_API_KEY=your_api_key")
            print("BINANCE_API_SECRET=your_api_secret")
            print("MOCK_MODE=true\n")
            sys.exit(1)
    else:
        logger.info("Running in mock mode - API keys not required")


@click.group()
def cli():
    """Trading Bot for Binance Futures Testnet (Mock Implementation)"""
    pass


@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading pair (e.g., BTCUSDT)')
@click.option('--side', '-d', required=True, type=click.Choice(['BUY', 'SELL']), help='Order side')
@click.option('--type', '-t', 'order_type', required=True, type=click.Choice(['MARKET', 'LIMIT']), help='Order type')
@click.option('--quantity', '-q', required=True, type=float, help='Order quantity')
@click.option('--price', '-p', type=float, help='Price for LIMIT orders (required for LIMIT)')
def place(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]):
    """Place a market or limit order"""
    
    logger.info(f"CLI command: place {symbol} {side} {order_type} {quantity} {price if price else ''}")
    
    try:
        # Validate environment
        validate_environment()
        
        # Initialize client
        client = BinanceFuturesClient(API_KEY, API_SECRET, testnet=TESTNET, mock_mode=MOCK_MODE)
        order_manager = OrderManager(client)
        
        # Place order
        result = order_manager.place_order(symbol, side, order_type, quantity, price)
        
        # Format and print output
        output = order_manager.format_order_output(result, symbol, side, order_type, quantity, price)
        print("\n" + output + "\n")
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\nValidation Error: {e}\n")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nError: {e}\n")
        sys.exit(1)


@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading pair')
@click.option('--order-id', '-i', required=True, type=int, help='Order ID to cancel')
def cancel(symbol: str, order_id: int):
    """Cancel an existing order"""
    
    try:
        validate_environment()
        
        client = BinanceFuturesClient(API_KEY, API_SECRET, testnet=TESTNET, mock_mode=MOCK_MODE)
        result = client.cancel_order(symbol, order_id)
        
        print("\n" + "=" * 50)
        print("ORDER CANCELLED")
        print("=" * 50)
        print(f"Symbol: {symbol}")
        print(f"Order ID: {order_id}")
        print(f"Status: {result.get('status')}")
        print("=" * 50)
        print("Successfully cancelled order\n")
        
        logger.info(f"Cancelled order {order_id} for {symbol}")
        
    except Exception as e:
        logger.error(f"Failed to cancel order: {e}")
        print(f"\nError cancelling order: {e}\n")
        sys.exit(1)


@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading pair')
def price(symbol: str):
    """Get current price for a symbol"""
    
    try:
        validate_environment()
        
        client = BinanceFuturesClient(API_KEY, API_SECRET, testnet=TESTNET, mock_mode=MOCK_MODE)
        current_price = client.get_symbol_price(symbol)
        
        print("\n" + "=" * 40)
        print(f"{symbol} Current Price: ${current_price:,.2f}")
        print("=" * 40 + "\n")
        
        logger.info(f"Retrieved price for {symbol}: {current_price}")
        
    except Exception as e:
        logger.error(f"Failed to get price: {e}")
        print(f"\nError: {e}\n")
        sys.exit(1)


@cli.command()
def status():
    """Check if bot is running and in what mode"""
    print("\n" + "=" * 50)
    print("TRADING BOT STATUS")
    print("=" * 50)
    print(f"Mode: {'MOCK' if MOCK_MODE else 'LIVE'}")
    print(f"API Key configured: {'Yes' if API_KEY and API_KEY != 'your_api_key_here' else 'No'}")
    print(f"Testnet: {TESTNET}")
    print("=" * 50)
    if MOCK_MODE:
        print("Running in MOCK MODE - All orders are simulated")
        print("   No real API calls are being made")
    print()


if __name__ == '__main__':
    cli()