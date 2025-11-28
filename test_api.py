from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret, testnet=True)

try:
    account_info = client.futures_account()
    print("✅ API Key Works! Connected to Binance Futures Testnet.")
    print("Available Balance:", account_info['totalWalletBalance'])
except Exception as e:
    print("❌ API Key Error:")
    print(e)
