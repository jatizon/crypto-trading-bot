class BotContext:
    def __init__(self, exchange, dispatcher, order_tracker, bot_config):
        self.exchange = exchange
        self.dispatcher = dispatcher
        self.order_tracker = order_tracker
        self.bot_config = bot_config
