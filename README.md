# Crypto Trading Bot

Event-oriented trading bot. The main loop does not make trading decisions. Decisions happen in event listeners that react when orders change status.

## Design Goals

The architecture separates orchestration, state, infrastructure, and reactive logic. That exists because a monolithic loop with trading logic spread throughout becomes hard to reason about and to change. Here, the loop only polls and emits; strategy lives in listeners.

## Execution Flow

1. The bot starts and places an order via `OrderTracker`.
2. `OrderTracker` polls the exchange and holds order state.
3. When an order status changes (e.g. closed), `OrderTracker` yields event names (`buy_order_closed`, `sell_order_closed`, etc.).
4. The main loop calls `EventDispatcher.emit()` with those events.
5. Listeners registered for that event run and decide what to do next (e.g. place a sell order, update balances).
6. New listeners can be wired for the new order; the loop continues polling.

The loop never knows *what* to do when an order closes. It only knows *that* something changed and forwards that to listeners.

## Layer Responsibilities

**TradingBot** – Orchestrates the lifecycle: place order, register listeners, loop and emit. Contains no strategy logic. Subclasses implement `run()` but the base pattern is: wire listeners, poll, emit. Strategy stays in listeners.

**BotContext** – Holds shared state (exchange, dispatcher, order_tracker, config, wallet). Passed into listeners so they don’t need globals or scattered dependencies. Everything a listener needs comes from context.

**EventDispatcher** – Decouples producers (the loop) from consumers (listeners). The loop emits events without knowing who reacts. Listeners register by event name. Producers and consumers stay independent.

**OrderTracker** – Encapsulates polling and order state. Calls the exchange, stores `Order` objects, detects status changes. Translates those changes into event names. The loop and listeners never touch raw exchange responses.

**Listeners** – Pure reactions. Functions like `on_buy_order_closed` and `on_sell_order_closed` contain the trading logic: compute sell price, place sell order, update balances. They receive `order_id` and `context`, and decide what to do. No orchestration, only reaction.

## Why This Architecture

**Events instead of direct calls** – `OrderTracker` has no idea what should happen when an order closes. That depends on the strategy. By emitting events, the tracker stays generic. Listeners, chosen by the strategy, handle the reaction. Change the strategy by changing listeners, not the tracker or the loop.

**Listeners as separate functions** – Logic is isolated and easy to test. You can swap listeners without touching the main loop. Each listener does one thing: react to a specific event. The loop stays small and predictable.

**Strategy ≠ infrastructure** – The loop, `OrderTracker`, `EventDispatcher`, and `BotContext` are reusable. They don’t depend on profit percentage, fee logic, or any particular strategy. All that lives in listeners. Add a new strategy by adding listeners; infrastructure stays the same.

## Project Structure

```
project/
├── pyproject.toml
├── bot_main.py
└── src/
    ├── helpers/
    │   ├── calculations.py
    │   ├── utils.py
    │   ├── get_historical_data.py
    │   └── market_data.py
    ├── events/
    │   ├── event_dispatcher.py
    │   ├── order_tracker.py
    │   └── order.py
    └── bot_files/
        ├── context.py
        ├── listeners.py
        ├── trading_bot.py
        └── trading_bot_example.py
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -e .
```

Requires Python 3.10+.

## Running

```bash
python bot_main.py
```

`bot_main.py` runs `TradingBotExample`. To use a different strategy, implement a subclass of `TradingBot` and wire your own listeners.

## Imports

Use package names directly. Never use `src` in imports:

```python
from helpers.calculations import convert_quote_to_base
from events.order_tracker import OrderTracker
from bot_files.context import BotContext
```

`pip install -e .` adds `src/` to `sys.path`, so `helpers`, `events`, and `bot_files` are top-level packages.
