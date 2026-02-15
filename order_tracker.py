from datetime import datetime

from order import Order


class OrderTracker:
    def __init__(self, exchange):
        self.exchange = exchange
        self.orders = {}

    def _place_order(self, symbol, order_type, side, amount, price=None):
        order = self.exchange.create_order(symbol, order_type, side, amount, price)
        return order

    def _track_order(self, order):
        order_id = order["id"]
        domain_order = Order.from_ccxt_order(order)
        self.orders[order_id] = domain_order

        # Identifying events at order creation
        event = self.create_event_for_order(domain_order, immediate_event=True)

        return order_id, event
        
    def place_and_track_order(self, symbol, order_type, side, amount, price=None):
        order = self._place_order(symbol, order_type, side, amount, price)
        return self._track_order(order)

    def update_order(self, order_id):
        old_order = self.get_order(order_id)
        symbol = old_order.symbol
        raw_order = self.exchange.fetch_order(order_id, symbol)
        order = old_order.update_from_ccxt(raw_order)
        self.orders[order_id] = order
        return order

    def get_order(self, order_id):
        return self.orders[order_id]

    def get_all_orders(self):
        return self.orders

    def remove_order(self, order_id):
        del self.orders[order_id]

    def create_event_for_order(self, order, old_order=None, immediate_event=False):
        if immediate_event or order.status != old_order.status:
            if order.status == "closed":
                return f"{order.side}_order_closed"
            if order.status == "canceled":
                return f"{order.side}_order_canceled"
            if order.status == "expired":
                return f"{order.side}_order_expired"
        return None

    def update_orders(self):
        event_order_ids = {}
        for order_id in list(self.orders):
            old_order = self.get_order(order_id) 
            order = self.update_order(order_id)

            event = self.create_event_for_order(order, old_order)
            if not event:
                continue
            if event not in event_order_ids:
                event_order_ids[event] = []
            event_order_ids[event].append(order_id)

        return event_order_ids
                

