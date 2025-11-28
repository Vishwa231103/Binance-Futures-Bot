# 🚀 Binance Futures Trading Bot (Python)

A simple, command-line trading bot built for **Binance Futures Testnet**.  
This project provides:

- Secure authentication using API keys  
- Market & Limit order placement  
- Order validation (precision, lot size, notional value)  
- Open order listing  
- Logging (file + console)  
- Fully modular bot structure  

This project **does not include any frontend UI**, as requested.

---

# 📂 Project Structure


trading/
│── basic_bot.py
│── cli.py
│── trading_cli.py
│── trading_bot.py
│── test_api.py
│── test_connection.py
│── .env
│── logs/
│ └── bot.log


---

# 🔐 Environment Setup

Create a `.env` file in your project folder:


BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com



---

# 🛠 Installation

```bash
pip install python-binance
pip install requests
pip install python-dotenv
pip install click


Testing API Connection
✔ Test 1: Verify API key

Run:

python test_api.py

✅ Sample Output
✅ API Key Works! Connected to Binance Futures Testnet.
Available Balance: 99.87650000


If incorrect:

❌ API Key Error:
APIError(code=-2015): Invalid API-key, IP, or permissions for action.

✔ Test 2: Check connection
python test_connection.py

Sample Output
✅ SUCCESS! Your Testnet API key works.
{ ... full futures account info ... }

📦 Using the CLI Bot

You can use cli.py or trading_cli.py.
Both perform the same actions.

🟢 1. Place a Market Order
python cli.py market BTCUSDT BUY 0.001

Sample Output
{
  "symbol": "BTCUSDT",
  "orderId": 24837463,
  "type": "MARKET",
  "status": "FILLED",
  "side": "BUY",
  "origQty": "0.001",
  "executedQty": "0.001",
  "avgPrice": "57123.50"
}

🟡 2. Place a Limit Order
python cli.py limit BTCUSDT SELL 0.002 56000

Sample Output
{
  "symbol": "BTCUSDT",
  "orderId": 24837470,
  "type": "LIMIT",
  "status": "NEW",
  "side": "SELL",
  "price": "56000",
  "origQty": "0.002",
  "timeInForce": "GTC"
}

🔍 3. Check Open Orders
python cli.py open-orders

Sample Output
{
  "symbol": "BTCUSDT",
  "orderId": 24837470,
  "status": "NEW",
  "price": "56000",
  "origQty": "0.002",
  "side": "SELL"
}


logs/bot.log
2025-11-27 09:05:00 | INFO | Bot initialized | Base URL: https://testnet.binancefuture.com
2025-11-27 09:05:01 | INFO | Exchange info fetched
2025-11-27 09:05:02 | INFO | Market order placed: {...}


🖥 Optional Interactive Script

Run the menu-based bot:

python trading_bot.py


Sample Output:

Options:
1 - List Open Orders
2 - Place Market Order
3 - Place Limit Order
0 - Exit

📌 Notes for Submission

All API keys must be stored in .env

There is no frontend UI

Logging enabled

Fully working test scripts included

Clean CLI interface for order placement

✔ Final Status

This bot is fully functional for:

Binance Futures Testnet

Market Orders

Limit Orders

Order Validation

Error Handling

Logging

CLI interface







