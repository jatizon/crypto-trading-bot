import time
from bot_files.context import BotContext
from bot_files.listeners import on_buy_order_closed
from helpers.calculations import convert_quote_to_base
from abc import ABC, abstractmethod
from bot_files.trading_bot import TradingBot


# Keep buying and selling at a profit percentage until ALL money is spent
class TradingBotExample(TradingBot):
    def run(self):
        buy_order_id = self.ctx.order_tracker.place_and_track_order(
            self.symbol, 
            "market", 
            "buy", 
            self.amount
        )

        self.dispatcher.add_event_listener(
            "buy_order_closed", 
            on_buy_order_closed,
            keep_listener=False, 
            expected_id=buy_order_id, 
            static_payload={"context": self.ctx},
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