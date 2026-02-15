from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Optional, Union, get_args, get_origin
import copy
from utils import now_seconds


@dataclass(slots=True)
class Order:
    id: str
    symbol: str
    side: str
    type: str

    amount: float
    filled: float
    remaining: float
    cost: Optional[float]
    average_price: Optional[float]
    target_price: Optional[float]

    creation_timestamp: int
    last_trade_timestamp: Optional[int]
    filled_timestamp: Optional[int]
    expiration_timestamp: Optional[int]

    cctx_status: str

    @property
    def status(self) -> str:
        if self.cctx_status != 'closed' and now_seconds() > self.expiration_timestamp:
            return "expired"
        return self.cctx_status

    @classmethod
    def from_ccxt_order(cls, order: Dict[str, Any], max_pending_time: int = 3600) -> "Order":
        if order["status"] == "closed":
            filled_ts = int(order["lastTradeTimestamp"]) if order["lastTradeTimestamp"] is not None else None
        else:
            filled_ts = None

        expiration_timestamp = int(order["timestamp"]) + max_pending_time

        return cls(
            # Fixed attributes
            id=str(order["id"]),
            symbol=str(order["symbol"]),
            side=str(order["side"]),
            type=str(order["type"]),
            amount=float(order["amount"]),
            creation_timestamp=int(order["timestamp"]),
            expiration_timestamp=expiration_timestamp,
            target_price=float(order["price"]) if order["price"] is not None else None,

            # Dynamic attributes
            cctx_status=str(order["status"]),
            filled=float(order["filled"]) if order["filled"] is not None else None,
            remaining=float(order["remaining"]) if order["remaining"] is not None else None,
            cost=float(order["cost"]) if order["cost"] is not None else None,
            average_price=float(order["average"]) if order["average"] is not None else None,
            last_trade_timestamp=int(order["lastTradeTimestamp"]) if order["lastTradeTimestamp"] is not None else None,
            filled_timestamp=filled_ts,
        )

    def update_from_ccxt(self, order: Dict[str, Any]) -> "Order":
        updated = copy.copy(self)

        if str(order["id"]) != self.id:
            raise ValueError("Cannot update Order with different id")

        if order["status"] == "closed" and self.filled_timestamp is None:
            filled_ts = int(order["lastTradeTimestamp"]) if order["lastTradeTimestamp"] is not None else None
        else:
            filled_ts = None

        # Update dynamic attributes
        updated.cctx_status = str(order["status"])
        updated.filled = float(order["filled"]) if order["filled"] is not None else None
        updated.remaining = float(order["remaining"]) if order["remaining"] is not None else None
        updated.cost = float(order["cost"]) if order["cost"] is not None else None
        updated.average_price = float(order["average"]) if order["average"] is not None else None
        updated.last_trade_timestamp = int(order["lastTradeTimestamp"]) if order["lastTradeTimestamp"] is not None else None
        updated.filled_timestamp = filled_ts

        return updated