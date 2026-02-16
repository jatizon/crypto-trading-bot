import time
from bot_files.context import BotContext
from bot_files.listeners import on_buy_order_closed
from helpers.calculations import convert_quote_to_base
from abc import ABC, abstractmethod

class TradingBot(ABC):
    def __init__(self, context: BotContext):
        self.ctx = context
        self.dispatcher = context.dispatcher
        self.order_tracker = context.order_tracker
        self.symbol = context.bot_config["symbol"]
        self.amount = convert_quote_to_base(
            self.ctx.exchange, 
            self.symbol, 
            self.ctx.bot_config["amount"]
        )

    @abstractmethod
    def run(self):
        pass
