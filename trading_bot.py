

import time
from context import BotContext
from listeners import on_buy_order_closed

class TradingBot:
    def __init__(self, context: BotContext):
        self.ctx = context
        self.dispatcher = context.dispatcher
        
    def run(self):
        print("Starting Bot...")
        
        symbol = self.ctx.bot_config["symbol"]
        amount = self.ctx.bot_config["amount"]
        
        buy_order_id, immediate_event = self.ctx.order_tracker.place_and_track_order(
            symbol, 
            "market", 
            "buy", 
            amount
        )

        listener = self.dispatcher.create_listener_for_id(buy_order_id, on_buy_order_closed)
        self.dispatcher.add_event_listener("order_closed", listener, keep_listener=False)

        if immediate_event:
            self.dispatcher.emit(immediate_event, id=buy_order_id, context=self.ctx)

        while True:
            events = self.ctx.order_tracker.update_orders()
            
            if events:
                for event_name, order_ids in events.items():
                    for order_id in order_ids:
                        self.dispatcher.emit(event_name, id=order_id, context=self.ctx)

            time.sleep(1)
    