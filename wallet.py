

class Wallet:
    def __init__(self, exchange):
        self.exchange = exchange

    def get_total_balance(self, currency):
        balance = self.exchange.fetch_balance()
        return balance[currency].get("total")

    def get_free_balance(self, currency):
        balance = self.exchange.fetch_balance()
        return balance[currency].get("free")

    def get_order(self, order_id):
        return self.exchange.fetch_order(order_id)

    def get_orders(self, symbol=None):
        return self.exchange.fetch_orders(symbol=symbol)