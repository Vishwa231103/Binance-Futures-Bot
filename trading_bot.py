from basic_bot import BasicBot

# Initialize the bot
bot = BasicBot()

def list_open_orders():
    print("Fetching open orders...")
    orders = bot.get_open_orders()
    if not orders:
        print("No open orders.")
    for o in orders:
        print(o)

def place_market_order():
    symbol = input("Symbol (e.g., BTCUSDT): ").upper()
    side = input("Side (BUY/SELL): ").upper()
    qty = float(input("Quantity: "))
    resp = bot.place_market_order(symbol, side, qty)
    print("Market Order Response:", resp)

def place_limit_order():
    symbol = input("Symbol (e.g., BTCUSDT): ").upper()
    side = input("Side (BUY/SELL): ").upper()
    qty = float(input("Quantity: "))
    price = float(input("Price: "))
    resp = bot.place_limit_order(symbol, side, qty, price)
    print("Limit Order Response:", resp)

def main():
    while True:
        print("\nOptions:")
        print("1 - List Open Orders")
        print("2 - Place Market Order")
        print("3 - Place Limit Order")
        print("0 - Exit")
        choice = input("Select option: ")

        if choice == "1":
            list_open_orders()
        elif choice == "2":
            place_market_order()
        elif choice == "3":
            place_limit_order()
        elif choice == "0":
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
