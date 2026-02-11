
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
    
def calculate_total_fee(exchange, symbol, usdc_amount, type):
    markets = exchange.load_markets()
    ticker = exchange.fetch_ticker(symbol)

    ask = ticker["ask"]
    bid = ticker["bid"]
    spread = ask - bid
    price = ticker["last"]

    if type == "market":
        exchange_fee = markets[symbol]['taker'] 
    elif type == "limit":
        exchange_fee = markets[symbol]['maker']

    total_fee = usdc_amount * (spread / price + exchange_fee)

    print(f'Total spread: {usdc_amount*spread/price} ({spread}/btc)')
    print(f'Total exchange fee: {usdc_amount*exchange_fee} ({(exchange_fee*100):.2f}%)')
    print(f'Total fee: {total_fee}')

    return total_fee