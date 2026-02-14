

import time
from context import BotContext
from listeners import on_buy_order_closed

class TradingBot:
    def __init__(self, context: BotContext):
        self.context = context
        
    def run(self):
        print("Starting Bot...")
        
        symbol = self.context.bot_config["symbol"]
        amount = self.context.bot_config["amount"]
        
        buy_order_id = self.context.order_tracker.create_order(symbol, "market", "buy", amount)

        listener = self.context.dispatcher.create_listener_for_id(buy_order_id, on_buy_order_closed)
        self.context.dispatcher.add_event_listener("order_closed", listener, keep_listener=False)

        while True:
            events = self.context.order_tracker.update_orders()
            
            if events:
                for event_name, order_ids in events.items():
                    print(f"Emitting event: {event_name}")
                    for order_id in order_ids:
                        self.context.dispatcher.emit(event_name, id=order_id, context=self.context)

            time.sleep(1)
    