from market_data import get_spread


def get_fee_pct(exchange, symbol, order_type):
    markets = exchange.load_markets()

    if order_type == "market":
        exchange_fee = markets[symbol]['taker'] 
    elif order_type == "limit":
        exchange_fee = markets[symbol]['maker']

    return exchange_fee

def get_operation_spread(exchange, symbol, amount):
    ticker = exchange.fetch_ticker(symbol)
    price = ticker["last"]

    spread = get_spread(exchange, symbol)

    spread_in_base = spread / price
    total_spread = amount * spread_in_base
    return total_spread


def sell_price_for_profit(quote_spent, amount_bought, profit_percentage, sell_fee):
    return quote_spent * (1 + profit_percentage) / (amount_bought * (1 - sell_fee))