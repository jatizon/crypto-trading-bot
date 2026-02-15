"""
Integration test for the trading bot with a real exchange.
Performs a 15 BRL buy, then sells, and verifies balance updates.

Requirements:
- Set BINANCE_API_KEY and BINANCE_API_SECRET in .env
- Run: python test_real_exchange.py
- Press Ctrl+C after both buy and sell orders complete to stop

This test verifies:
1. Buy order is placed correctly
2. Sell order is placed when buy fills
3. Balances are updated correctly after buy and sell
"""
import os
import sys
import ccxt
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from market_data import get_total_balance
from trading_bot import TradingBot
from event_dispatcher import EventDispatcher
from order_tracker import OrderTracker
from context import BotContext
from listeners import on_sell_order_closed

load_dotenv()

# --- Configuration for 15 BRL test (Binance) ---
EXCHANGE_CLASS = ccxt.binance
API_KEY_ENV = "BINANCE_API_KEY"
API_SECRET_ENV = "BINANCE_API_SECRET"
SYMBOL = "BTC/BRL"
QUOTE_CURRENCY = "BRL"
BASE_CURRENCY = "BTC"
QUOTE_AMOUNT = 15  # 15 BRL for market buy (will be converted to BTC amount)

# --- Logging for verification ---
def make_logging_listener(name):
    def listener(order_id=None, context=None, delta_balances=None, **kwargs):
        print(f"\n[TEST] {name}: order_id={order_id}")
        if delta_balances:
            print(f"       delta_balances: {delta_balances}")
        if context:
            print(f"       context.balances (before): BRL={context.balances.get('BRL', 0)}, BTC={context.balances.get('BTC', 0)}")
            if delta_balances:
                after_brl = context.balances.get("BRL", 0) + delta_balances.get("BRL", 0)
                after_btc = context.balances.get("BTC", 0) + delta_balances.get("BTC", 0)
                print(f"       context.balances (after update): BRL={after_brl}, BTC={after_btc}")
        return True, None
    return listener


def main():
    api_key = os.getenv(API_KEY_ENV)
    api_secret = os.getenv(API_SECRET_ENV)
    if not api_key or not api_secret:
        print(f"Error: Set {API_KEY_ENV} and {API_SECRET_ENV} in .env")
        sys.exit(1)

    exchange = EXCHANGE_CLASS({
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True,
    })
    if hasattr(exchange, "options"):
        exchange.options["createMarketBuyOrderRequiresPrice"] = False

    # Convert 15 BRL to BTC amount (Binance expects amount in base currency, must match LOT_SIZE)
    exchange.load_markets()
    ticker = exchange.fetch_ticker(SYMBOL)
    price = ticker["last"]
    amount_btc_raw = QUOTE_AMOUNT / price
    amount_btc = float(exchange.amount_to_precision(SYMBOL, amount_btc_raw))
    if amount_btc <= 0:
        print(f"Error: Calculated amount {amount_btc} BTC is too small (15 BRL @ {price} BRL/BTC)")
        sys.exit(1)

    bot_config = {
        "symbol": SYMBOL,
        "type": "market",
        "side": "buy",
        "amount": amount_btc,
        "profit_percentage": 0.0001,  # 0.01% profit target
    }

    print(f"  Market: {SYMBOL} @ {price} BRL | Order: {amount_btc} BTC (~{QUOTE_AMOUNT} BRL)")

    # Initial balances from exchange (before any trade)
    initial_brl = get_total_balance(exchange, QUOTE_CURRENCY)
    initial_btc = get_total_balance(exchange, BASE_CURRENCY)
    print(f"\n=== INITIAL BALANCES (from exchange) ===")
    print(f"  {QUOTE_CURRENCY}: {initial_brl}")
    print(f"  {BASE_CURRENCY}: {initial_btc}")

    dispatcher = EventDispatcher()
    order_tracker = OrderTracker(exchange)
    context = BotContext(exchange, dispatcher, order_tracker, bot_config)

    # Add sell_order_closed listener (not wired in trading_bot.py - needed for balance update on sell)
    def sell_listener(order_id, context=None, **kwargs):
        if context:
            result = on_sell_order_closed(order_id=order_id, context=context)
            print(f"\n[TEST] SELL ORDER CLOSED: order_id={order_id}")
            print(f"       Final context.balances: BRL={context.balances['BRL']}, BTC={context.balances['BTC']}")
            return True, result
        return False, None

    dispatcher.add_event_listener("sell_order_closed", sell_listener, keep_listener=True)

    # Add logging listeners to verify events
    dispatcher.add_event_listener(
        "update_balances",
        make_logging_listener("UPDATE_BALANCES"),
        keep_listener=True,
        static_payload={"context": context},
    )

    # Log when buy order closes (before sell is placed)
    def buy_closed_logger(order_id, context=None, **kwargs):
        print(f"\n[TEST] BUY ORDER CLOSED: order_id={order_id} - sell order will be placed next")
        return True, None

    dispatcher.add_event_listener("buy_order_closed", buy_closed_logger, keep_listener=True)

    print(f"\n=== STARTING BOT: buy ~{QUOTE_AMOUNT} {QUOTE_CURRENCY} ({amount_btc} BTC) of {SYMBOL} ===")
    print("Watch for [TEST] logs. Press Ctrl+C after both orders complete.\n")

    bot = TradingBot(context)
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\n=== FINAL VERIFICATION ===")
        print(f"context.balances (tracked): BRL={context.balances['BRL']}, BTC={context.balances['BTC']}")
        final_brl = get_total_balance(exchange, QUOTE_CURRENCY)
        final_btc = get_total_balance(exchange, BASE_CURRENCY)
        print(f"Exchange balances: {QUOTE_CURRENCY}={final_brl}, {BASE_CURRENCY}={final_btc}")
        print("\nVerify: context.balances should match exchange balances if all updates ran correctly.")


if __name__ == "__main__":
    main()
