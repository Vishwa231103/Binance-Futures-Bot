import click
from basic_bot import BasicBot

bot = BasicBot()

@click.group()
def cli():
    pass

@cli.command()
def open_orders():
    """List all open orders"""
    orders = bot.get_open_orders()
    for o in orders:
        print(o)

@cli.command()
@click.argument("symbol")
@click.argument("side")
@click.argument("quantity", type=float)
@click.argument("price", type=float)
def limit(symbol, side, quantity, price):
    resp = bot.place_limit_order(symbol, side, quantity, price)
    print(resp)

@cli.command()
@click.argument("symbol")
@click.argument("side")
@click.argument("quantity", type=float)
def market(symbol, side, quantity):
    resp = bot.place_market_order(symbol, side, quantity)
    print(resp)

if __name__ == "__main__":
    cli()
