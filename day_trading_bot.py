

from wallet import Wallet


class DayTradingBot:
    def __init__(self, exchange, dispatcher, order_tracker, bot_config):
        self.bot_config = bot_config

        self.exchange = exchange
        self.dispatcher = dispatcher
        self.order_tracker = order_tracker

    def create_order(self, symbol, type, side, amount, price=None):
        raw_order = self.exchange.create_order(symbol, type, side, amount, price)
        finished_order = self.exchange.fetch_order(raw_order["id"])
        return finished_order

    def run(self):
        while True:
            self.dispatcher.add_event_listener(
                "order_confirmed",
                self.wallet.sell_coin,
                symbol=self.symbol,
                type="market",
                btc_amount=order.amount,
                keep_listener=True,
            )
            self.dispatcher.emit("order_created", order=finished_order)