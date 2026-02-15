import time
from context import BotContext
from listeners import on_buy_order_closed, on_update_balances

class TradingBot:
    def __init__(self, context: BotContext):
        self.ctx = context
        self.dispatcher = context.dispatcher
        self.order_tracker = context.order_tracker
        self.symbol = context.bot_config["symbol"]
        self.amount = context.bot_config["amount"]
            
    def run(self):
        buy_order_id, immediate_event = self.ctx.order_tracker.place_and_track_order(
            self.symbol, 
            "market", 
            "buy", 
            self.amount
        )

        self.dispatcher.add_event_listener(
            "update_balances", 
            on_update_balances, 
            keep_listener=True, 
            static_payload={"context": self.ctx}
        )

        self.dispatcher.add_event_listener(
            "buy_order_closed", 
            on_buy_order_closed,
            keep_listener=False, 
            expected_id=buy_order_id, 
            static_payload={"context": self.ctx},
        )

        if immediate_event:
            self.dispatcher.emit(
                immediate_event, 
                order_id=buy_order_id, 
                event_payload={"context": self.ctx}
            )

        while True:
            events = self.ctx.order_tracker.update_orders()
            
            if events:
                for event_name, order_ids in events.items():
                    for order_id in order_ids:
                        self.dispatcher.emit(
                            event_name, 
                            order_id=order_id, 
                            event_payload={"context": self.ctx}
                        )

            time.sleep(1)
    