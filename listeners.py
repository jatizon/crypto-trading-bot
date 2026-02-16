from calculations import get_fee_pct, sell_price_for_profit

# Example of listeners to buy and sell at a profit percentage

def on_buy_order_closed(order_id, context):    
    buy_order = context.order_tracker.get_order(order_id)

    filled_amount = buy_order.filled
    cost = buy_order.cost
    symbol = context.bot_config["symbol"]

    context.wallet["runtime_balances"]["BRL"] += -cost
    context.wallet["runtime_balances"]["BTC"] += filled_amount

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
        sell_price,
    )

    context.dispatcher.add_event_listener(
        "sell_order_closed", 
        on_sell_order_closed,
        keep_listener=False, 
        expected_id=sell_order_id, 
        static_payload={"context": context, "buy_cost": cost},
    )

def on_sell_order_closed(order_id, context, buy_cost):
    sell_order = context.order_tracker.get_order(order_id)

    filled_amount = sell_order.filled
    cost = sell_order.cost

    profit = cost - buy_cost
    profit_pct = profit / buy_cost

    context.wallet["runtime_balances"]["BRL"] += cost
    context.wallet["runtime_balances"]["BTC"] += -filled_amount
    context.wallet["total_profit"] += profit

    print(f"Profit: {profit}, Profit Percentage: {profit_pct}")
    print(f"Runtime Balances: {context.wallet['runtime_balances']}")
    print(f"Total Profit: {context.wallet['total_profit']}")