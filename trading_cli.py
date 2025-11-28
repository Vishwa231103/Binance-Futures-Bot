# trading_cli.py
import argparse
import sys
from basic_bot import BasicBot
import logging

# Initialize bot
bot = BasicBot()
logger = logging.getLogger("BasicBot")

def place_market(symbol, side, quantity):
    try:
        resp = bot.place_market_order(symbol, side.upper(), quantity)
        logger.info("Market order placed successfully")
        print(resp)
    except Exception as e:
        logger.error("Error placing market order: %s", e)
        print("Error:", e)

def place_limit(symbol, side, quantity, price):
    try:
        resp = bot.place_limit_order(symbol, side.upper(), quantity, price)
        logger.info("Limit order placed successfully")
        print(resp)
    except Exception as e:
        logger.error("Error placing limit order: %s", e)
        print("Error:", e)

def list_open_orders():
    try:
        orders = bot.get_open_orders()
        logger.info("Fetched open orders successfully")
        if orders:
            for o in orders:
                print(o)
        else:
            print("No open orders")
    except Exception as e:
        logger.error("Error fetching open orders: %s", e)
        print("Error:", e)

def main():
    parser = argparse.ArgumentParser(description="Trading Bot CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Market order
    market_parser = subparsers.add_parser("market", help="Place a market order")
    market_parser.add_argument("symbol")
    market_parser.add_argument("side")
    market_parser.add_argument("quantity", type=float)

    # Limit order
    limit_parser = subparsers.add_parser("limit", help="Place a limit order")
    limit_parser.add_argument("symbol")
    limit_parser.add_argument("side")
    limit_parser.add_argument("quantity", type=float)
    limit_parser.add_argument("price", type=float)

    # Open orders
    subparsers.add_parser("open_orders", help="List all open orders")

    args = parser.parse_args()

    if args.command == "market":
        place_market(args.symbol, args.side, args.quantity)
    elif args.command == "limit":
        place_limit(args.symbol, args.side, args.quantity, args.price)
    elif args.command == "open_orders":
        list_open_orders()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
