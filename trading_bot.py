import time
from context import BotContext
from listeners import on_buy_order_closed
from calculations import convert_quote_to_base

class TradingBot:
    def __init__(self, context: BotContext):
        self.ctx = context
        self.dispatcher = context.dispatcher
        self.order_tracker = context.order_tracker
        self.symbol = context.bot_config["symbol"]
        self.amount = convert_quote_to_base(self.ctx.exchange, self.symbol, context.bot_config["amount"])

    def run(self):
        pass