import time
import uuid
from typing import Dict, Any, Optional

class MockBinance:
    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}

    def create_order(self, symbol: str, type: str, side: str, amount: float, price: Optional[float] = None) -> Dict[str, Any]:
        order_id = str(uuid.uuid4())
        timestamp = int(time.time() * 1000)
        
        order = {
            "id": order_id,
            "clientOrderId": None,
            "symbol": symbol,
            "side": side,
            "type": type,
            "amount": amount,
            "filled": 0.0,
            "remaining": amount,
            "cost": 0.0,
            "average": None,
            "status": "open",
            "timestamp": timestamp,
            "datetime":  time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(timestamp/1000)),
            "lastTradeTimestamp": None,
            "info": {},
            "fee": None,
            "trades": []
        }
        
        self.orders[order_id] = order
        return order

    def fetch_order(self, id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        if id in self.orders:
            return self.orders[id]
        raise Exception(f"Order {id} not found")

    # Helper to simulate state changes from the "exchange" side
    def update_order_status(self, order_id: str, status: str, filled: Optional[float] = None):
        if order_id in self.orders:
            self.orders[order_id]["status"] = status
            if filled is not None:
                self.orders[order_id]["filled"] = filled
                self.orders[order_id]["remaining"] = self.orders[order_id]["amount"] - filled
                if filled > 0:
                     self.orders[order_id]["lastTradeTimestamp"] = int(time.time() * 1000)
