import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Initialize the futures testnet client
client = Client(API_KEY, API_SECRET, testnet=True)

try:
    account_info = client.futures_account()
    print("✅ SUCCESS! Your Testnet API key works.")
    print(account_info)
except Exception as e:
    print("❌ ERROR: API key is not working.")
    print(e)
