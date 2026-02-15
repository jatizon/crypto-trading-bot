from calculations import get_fee_pct, sell_price_for_profit


def on_buy_order_closed(order_id=None, context=None):    
    buy_order = context.order_tracker.get_order(order_id)

    filled_amount = buy_order.filled
    cost = buy_order.cost
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

    delta_balances = {
        "BRL": -cost,
        "BTC": filled_amount,
    }
    context.dispatcher.emit(
        "update_balances", 
        event_payload={"delta_balances": delta_balances},
    )

def on_sell_order_closed(order_id=None, context=None):
    sell_order = context.order_tracker.get_order(order_id)

    filled_amount = sell_order.filled
    cost = sell_order.cost

    delta_balances = {
        "BRL": cost,
        "BTC": -filled_amount,
    }
    context.dispatcher.emit(
        "update_balances", 
        event_payload={"delta_balances": delta_balances},
    )

def on_update_balances(context=None, delta_balances=None):
    context.balances["BRL"] += delta_balances["BRL"]
    context.balances["BTC"] += delta_balances["BTC"]
    return True, None