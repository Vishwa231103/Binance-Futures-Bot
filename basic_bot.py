# basic_bot.py
import os
import time
import hmac
import hashlib
import logging
from logging.handlers import RotatingFileHandler
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

load_dotenv()

# ---------------- LOGGING SETUP ----------------
logger = logging.getLogger("BasicBot")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = RotatingFileHandler("logs/bot.log", maxBytes=5_000_000, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)


class BasicBot:
    def __init__(self, api_key=None, api_secret=None, base_url=None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = base_url or os.getenv("BINANCE_BASE_URL")

        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key or secret")

        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.info("Bot initialized | Base URL: %s", self.base_url)

    # ---------------- Binance Core Methods ----------------
    def get_exchange_info(self):
        resp = self.session.get(self.base_url + "/fapi/v1/exchangeInfo", timeout=10)
        resp.raise_for_status()
        logger.info("Exchange info fetched")
        return resp.json()

    def get_symbol_info(self, symbol):
        symbol = symbol.upper()
        data = self.get_exchange_info()

        for s in data["symbols"]:
            if s["symbol"] == symbol:
                return {
                    "symbol": symbol,
                    "pricePrecision": s["pricePrecision"],
                    "quantityPrecision": s["quantityPrecision"],
                    "filters": {f["filterType"]: f for f in s["filters"]},
                }

        raise ValueError(f"Symbol {symbol} not found")

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params):
        query = urlencode(params, doseq=True)
        return hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()

    def _send_signed_request(self, method, endpoint, params):
        url = self.base_url + endpoint
        params["timestamp"] = self._get_timestamp()
        params["signature"] = self._sign(params)

        logger.debug("Request: %s %s params=%s", method, url, params)

        resp = (
            self.session.post(url, params=params)
            if method == "POST"
            else self.session.get(url, params=params)
        )

        logger.debug("Response: %s %s", resp.status_code, resp.text)
        resp.raise_for_status()
        return resp.json()

    # ---------------- Order Validation ----------------
    def validate_order(self, symbol, price=None, quantity=None):
        info = self.get_symbol_info(symbol)
        filters = info["filters"]

        # ---- FIX FOR FUTURES TESTNET ----
        if "MIN_NOTIONAL" in filters:
            min_notional = float(filters["MIN_NOTIONAL"]["minNotional"])
        elif "NOTIONAL" in filters:
            min_notional = float(filters["NOTIONAL"]["notional"])
        else:
            raise ValueError("No notional filter found for this symbol")

        # Price rounding
        if price is not None:
            tick = float(filters["PRICE_FILTER"]["tickSize"])
            price = round((float(price) // tick) * tick, info["pricePrecision"])

        # Quantity rounding
        if quantity is not None:
            step = float(filters["LOT_SIZE"]["stepSize"])
            quantity = round((float(quantity) // step) * step, info["quantityPrecision"])

        # Notional calculation
        last_price = price if price else self.get_last_price(symbol)
        notional = last_price * quantity

        if notional < min_notional:
            raise ValueError(
                f"Order notional {notional} is below minimum allowed {min_notional}"
            )

        return price, quantity

    def get_last_price(self, symbol):
        resp = self.session.get(self.base_url + "/fapi/v1/ticker/price", params={"symbol": symbol})
        resp.raise_for_status()
        return float(resp.json()["price"])

    # ---------------- Order Methods ----------------
    def place_market_order(self, symbol, side, quantity):
        _, qty = self.validate_order(symbol, quantity=quantity)

        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "MARKET",
            "quantity": qty,
        }

        resp = self._send_signed_request("POST", "/fapi/v1/order", params)
        logger.info("Market order placed: %s", resp)
        return resp

    def place_limit_order(self, symbol, side, quantity, price):
        price, qty = self.validate_order(symbol, price=price, quantity=quantity)

        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "LIMIT",
            "timeInForce": "GTC",
            "price": price,
            "quantity": qty,
        }

        resp = self._send_signed_request("POST", "/fapi/v1/order", params)
        logger.info("Limit order placed: %s", resp)
        return resp

    def get_open_orders(self):
        resp = self._send_signed_request("GET", "/fapi/v1/openOrders", {})
        logger.info("Fetched open orders successfully")
        return resp
