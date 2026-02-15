from calculations import get_fee_pct, sell_price_for_profit


def on_buy_order_closed(id=None, context=None, **kwargs):    
    buy_order = context.order_tracker.get_order(id)

    filled_amount = buy_order['filled']
    cost = buy_order['cost']
    symbol = context.bot_config["symbol"]

    sell_fee = get_fee_pct(context.exchange, symbol, "limit")

    sell_price = sell_price_for_profit(
        cost,
        filled_amount,
        context.bot_config["profit_percentage"],
        sell_fee
    )
    
    sell_order_id = context.order_tracker.place_and_track_order(
        symbol,
        "limit",
        "sell",
        filled_amount,
        sell_price
    )

def on_sell_order_closed(id=None, context=None, **kwargs):
