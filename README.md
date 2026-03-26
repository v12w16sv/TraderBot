# Trading Bot - Binance Futures Testnet (Mock Implementation)

A Python-based trading bot with clean architecture, comprehensive logging, and mock mode for testing.

## Features

- Place MARKET and LIMIT orders (mock simulation)
- Support BUY and SELL sides
- Input validation for all parameters
- Comprehensive logging to file and console
- Error handling for invalid inputs
- Clean CLI interface using Click
- Mock mode for testing without real API keys

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher

### 2. Installation

```bash
# Navigate to project folder
cd trading_bot

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt