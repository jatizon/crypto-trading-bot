
def get_total_balance(exchange, currency):
    balance = exchange.fetch_balance()
    return balance[currency].get("total")

def get_free_balance(exchange, currency):
    balance = exchange.fetch_balance()
    return balance[currency].get("free")

def buy_coin(exchange, symbol, type, usdc_amount, price=None):
    raw_order = exchange.create_order(symbol, type, side="buy", amount=usdc_amount, price=price)
    finished_order = exchange.fetch_order(raw_order["id"])
    return finished_order

def sell_coin(exchange, symbol, type, btc_amount, price=None):
    raw_order = exchange.create_order(symbol, type, side="sell", amount=btc_amount, price=price)
    finished_order = exchange.fetch_order(raw_order["id"])
    return finished_order

def get_order(exchange, order_id):
    return exchange.fetch_order(order_id)

def get_orders(exchange, symbol=None):
    return exchange.fetch_orders(symbol=symbol)