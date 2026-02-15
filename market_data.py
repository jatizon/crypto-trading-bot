
def get_best_bid(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker["bid"]

def get_best_ask(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker["ask"]

def get_spread(exchange, symbol):
    bid = get_best_bid(exchange, symbol)
    ask = get_best_ask(exchange, symbol)
    return ask - bid
    
def get_price(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker["last"]

def get_total_balance(exchange, currency):
        balance = exchange.fetch_balance()
        return balance[currency].get("total")

def get_free_balance(exchange, currency):
        balance = exchange.fetch_balance()
        return balance[currency].get("free")