import time

class DayTradingBot:
    def __init__(self, exchange, market_data, wallet):
        self.exchange = exchange
        self.market_data = market_data
        self.wallet = wallet

        self.selling_orders = {'PENDING': [], 'FILLED': []}

        self.profit_percentage = 0.1
        self.usdc_buy_amount = 1
        self.symbol = 'BTC/USDC'
        self.sell_after_minutes = 60
        self.max_invested_usdc = 10

    def run(self):
        while True:
            current_timestamp = time.time()
            order = self.wallet.buy_coin(self.exchange, self.symbol, "market", self.usdc_buy_amount)
