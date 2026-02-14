

import time

class DayTradingBot:
    def __init__(self, exchange, dispatcher, order_tracker, bot_config):
        self.bot_config = bot_config

        self.exchange = exchange
        self.dispatcher = dispatcher
        self.order_tracker = order_tracker

    def run(self):
        print("Starting Bot...")
        
        symbol = self.bot_config["symbol"]
        amount = self.bot_config["amount"]
        
        print(f"Creating market buy order for {amount} USD of {symbol}...")
        buy_order_id = self.order_tracker.create_order(symbol, "market", "buy", amount)
        print(f"Buy order created: {buy_order_id}")

        def on_buy_order_closed(order_id=None, **kwargs):
            print(f"Buy order {order_id} closed! Creating sell order...")
            
            buy_order = self.order_tracker.get_order(order_id)
            filled_amount = buy_order['filled']
            average_price = buy_order['average']
            
            if filled_amount > 0:
                print(f"Placing limit sell order for {filled_amount} {symbol} at {average_price}")
                sell_order_id = self.order_tracker.create_order(symbol, "limit", "sell", filled_amount, average_price)
                print(f"Sell order created: {sell_order_id}")
            else:
                print("Order finished but no amount filled?")

        listener = self.dispatcher.create_listener_for_id(buy_order_id, on_buy_order_closed)
        self.dispatcher.add_event_listener("order_closed", listener, keep_listener=False)

        print("Entering monitoring loop...")
        while True:
            events = self.order_tracker.update_orders()
            
            if events:
                for event_name, order_ids in events.items():
                    print(f"Emitting event: {event_name}")
                    for order_id in order_ids:
                        self.dispatcher.emit(event_name, id=order_id, order_id=order_id)

            time.sleep(1)
    