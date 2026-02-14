from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Optional, Union, get_args, get_origin


@dataclass(slots=True)
class Order:
    # ---- core identifiers ----
    id: str
    client_order_id: Optional[str]
    symbol: str
    side: str
    type: str

    # ---- quantities & price ----
    amount: float
    filled: float
    remaining: float
    cost: Optional[float]
    average_price: Optional[float]

    # ---- status & time ----
    status: str
    timestamp: int                 # order creation / exchange timestamp
    datetime: str
    last_trade_timestamp: Optional[int]      # timestamp of last execution
    filled_timestamp: Optional[int]          # moment order became fully filled

    # ---- raw / exchange specific ----
    info: Dict[str, Any] = field(repr=False)

    # ---- optional / future ----
    fee: Optional[Any]
    trades: List[Any]

    # ---- custom user fields ----
    metadata: Dict[str, Any] = field(default_factory=dict)

    # ==========================
    # Factory
    # ==========================
    @classmethod
    def from_ccxt_order(cls, order: Dict[str, Any]) -> "Order":
        try:
            last_trade_ts = int(order["lastTradeTimestamp"])
            timestamp = int(order["timestamp"])

            filled_timestamp = last_trade_ts if order["status"] == "FILLED" else None

            return cls(
                # identifiers
                id=str(order["id"]),
                client_order_id=order.get("clientOrderId"),
                symbol=str(order["symbol"]),
                side=str(order["side"]),
                type=str(order["type"]),

                # quantities
                amount=float(order["amount"]),
                filled=float(order["filled"]),
                remaining=float(order["remaining"]),
                cost=float(order["cost"]) if order["cost"] is not None else None,
                average_price=float(order["average"]) if order["average"] is not None else None,

                # time & status
                status=str(order["status"]),
                timestamp=timestamp,
                datetime=str(order["datetime"]),
                last_trade_timestamp=last_trade_ts,
                filled_timestamp=filled_timestamp,

                # raw
                info=dict(order["info"]),

                # optional
                fee=order.get("fee"),
                trades=list(order.get("trades", [])),
            )

        except KeyError as e:
            raise KeyError(f"Missing required order field: {e}") from e
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid order field type: {e}") from e

    def _is_instance(value, expected_type) -> bool:
        origin = get_origin(expected_type)

        if origin is Union:
            return any(_is_instance(value, t) for t in get_args(expected_type))

        if expected_type is Any:
            return True

        return isinstance(value, expected_type)
        
    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            expected = f.type

            if value is None:
                # Allow None only if Optional
                origin = get_origin(expected)
                if origin is not Union or type(None) not in get_args(expected):
                    raise TypeError(f"{f.name} is None but expected {expected}")
                continue

            if not _is_instance(value, expected):
                raise TypeError(
                    f"{f.name}={value!r} has type {type(value)}, expected {expected}"
                )
