def on_buy_order_closed(id=None, context=None, **kwargs):
    print(f"Buy order {id} closed! Creating sell order...")
    
    buy_order = context.order_tracker.get_order(id)
    filled_amount = buy_order['filled']
    average_price = buy_order['average']
    symbol = context.bot_config["symbol"]
    
    if filled_amount > 0:
        print(f"Placing limit sell order for {filled_amount} {symbol} at {average_price}")
        sell_order_id = context.order_tracker.create_order(symbol, "limit", "sell", filled_amount, average_price)
        print(f"Sell order created: {sell_order_id}")
    else:
        print("Order finished but no amount filled?")
