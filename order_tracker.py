from datetime import datetime
import copy
from order import Order


class OrderTracker:
    def __init__(self, exchange):
        self.exchange = exchange
        self.orders = {}
        self.immediate_events = {}

    def log_order(self, domain_order):
        print("="*35)
        print(f"Order Placed:")
        print(f"  Order ID: {domain_order.id}")
        print(f"  Symbol: {domain_order.symbol}")
        print(f"  Side: {domain_order.side}")
        print(f"  Type: {domain_order.type}")
        print(f"  Status: {domain_order.status}")
        print(f"  Average Price: {domain_order.average_price}")
        print(f"  Amount: {domain_order.amount}")
        print(f"  Filled: {domain_order.filled}")
        print(f"  Remaining: {domain_order.remaining}")
        print(f"  Cost: {domain_order.cost}")
        print(f"  Creation Time: {domain_order.creation_timestamp}")
        print(f"  Target Price: {domain_order.target_price}")
        print("="*35)

    def _place_order(self, symbol, order_type, side, amount, price=None):
        order = self.exchange.create_order(symbol, order_type, side, amount, price)
        return order

    def _track_order(self, order):
        order_id = order["id"]
        domain_order = Order.from_ccxt_order(order)
        self.orders[order_id] = domain_order

        self.log_order(domain_order)

        # Identifying events at order creation
        immediate_event = self.create_event_for_order(domain_order, immediate_event=True)

        return order_id, immediate_event
        
    def place_and_track_order(self, symbol, order_type, side, amount, price=None):
        order = self._place_order(symbol, order_type, side, amount, price)
        order_id, immediate_event = self._track_order(order)

        if not immediate_event:
            return order_id
        if immediate_event not in self.immediate_events:
            self.immediate_events[immediate_event] = []
        self.immediate_events[immediate_event].append(order_id)

        return order_id

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

    def create_event_for_order(self, order, old_order=None, immediate_event=False):
        if immediate_event or (old_order and order.status != old_order.status):
            if order.status == "closed":
                return f"{order.side}_order_closed"
            if order.status == "canceled":
                return f"{order.side}_order_canceled"
            if order.status == "expired":
                return f"{order.side}_order_expired"
        return None

    def update_orders(self):
        # Get immediate events
        event_order_ids = copy.deepcopy(self.immediate_events)
        self.immediate_events.clear()

        # Get normal events
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
