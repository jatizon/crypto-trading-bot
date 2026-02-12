import time

class DayTradingBot:
    def __init__(self, exchange, market_data, wallet):
        self.exchange = exchange
        self.market_data = market_data
        self.wallet = wallet

        self.profit_percentage = 0.1
        self.usdc_buy_amount = 1
        self.symbol = 'BTC/USDC'
        self.sell_after_minutes = 60
        self.max_invested_usdc = 10

        self.event_listeners = {}

    def add_event_listener(self, event, listener, keep_listener=False, **kwargs):
        if event not in self.event_listeners:
            self.event_listeners[event] = []
        self.event_listeners[event].append((listener, keep_listener, kwargs))

    def update_event_listeners(self):
        for event in list(self.event_listeners.keys()):
            if self.event_listeners[event] == []:
                del self.event_listeners[event]
                continue
            if event():
                for elements in self.event_listeners[event].copy():
                    listener, keep_listener, listener_kwargs = elements
                    listener(**listener_kwargs)
                    if not keep_listener:
                        self.event_listeners[event].remove(elements)

    def run(self):
        while True:
            current_timestamp = time.time()
            order = self.wallet.buy_coin(self.exchange, self.symbol, "market", self.usdc_buy_amount)
            self.add_event_listener(
                lambda: order.status == "closed",
                lambda: self.wallet.sell_coin(self.exchange, self.symbol, "market", order.amount),
                keep_listener=True,
            )
            self.update_event_listeners()
