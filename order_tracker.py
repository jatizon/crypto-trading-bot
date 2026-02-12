



class OrderTracker:
    def __init__(self, exchange):
        self.exchange = exchange
        self.orders = {}

    def get_status(self, order_id):
        return self.orders[order_id]["status"]

    def create_order(self, symbol, order_type, side, amount, price=None):
        order = self.exchange.create_order(symbol, order_type, side, amount, price)
        order_id = order["id"]
        self.orders[order_id] = order
        return order_id

    def get_order(self, order_id):
        return self.orders.get(order_id)

    def get_orders(self):
        return self.orders

    def remove_order(self, order_id):
        del self.orders[order_id]

    def create_event(self, prev_status, status, order_id):
        if status == prev_status:
            return None
        if status == "closed":
            return {"name": "order_closed", "order_id": order_id}
        if status == "canceled":
            return {"name": "order_canceled", "order_id": order_id}

    def update_order(self, order_id):
        self.orders[order_id] = self.exchange.fetch_order(order_id)
        return self.orders[order_id]

    def update_orders(self):
        events = {}
        for order_id in self.orders:
            prev_status = self.get_status(order_id)
            order = self.update_order(order_id)
            status = order["status"]

            event = self.create_event(prev_status, status, order_id)
            if event:
                if event["name"] not in events:
                    events[event["name"]] = []
                events[event["name"]].append(event)
                

