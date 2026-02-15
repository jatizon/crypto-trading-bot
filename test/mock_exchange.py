from typing import Any, Dict, List, Optional


class MockExchange:
    """Mock exchange that implements all ccxt exchange methods used in the codebase."""

    def __init__(self):
        pass

    # ── Order Management ─────────────────────────────────────────────

    def create_order(
        self,
        symbol: str,
        type: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def fetch_order(self, id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        raise NotImplementedError

    def fetch_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        raise NotImplementedError

    # ── Market Data ──────────────────────────────────────────────────

    def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        raise NotImplementedError

    def load_markets(self) -> Dict[str, Any]:
        raise NotImplementedError

    # ── Wallet / Balance ─────────────────────────────────────────────

    def fetch_balance(self) -> Dict[str, Any]:
        raise NotImplementedError

    # ── Test Helpers (simulate exchange-side state changes) ──────────

    def fill_order(self, order_id: str, filled: Optional[float] = None) -> None:
        """Simulate an order being fully or partially filled."""
        raise NotImplementedError

    def cancel_order(self, order_id: str) -> None:
        """Simulate an order being canceled by the exchange."""
        raise NotImplementedError

    def set_ticker(self, symbol: str, bid: float, ask: float, last: float) -> None:
        """Set the ticker data that fetch_ticker will return."""
        raise NotImplementedError

    def set_balance(self, currency: str, free: float, total: float) -> None:
        """Set the balance data that fetch_balance will return."""
        raise NotImplementedError