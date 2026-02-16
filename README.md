# Crypto Trading Bot

Python bot that places orders, tracks their status, and reacts to events (order closed, canceled, etc.). Uses an abstract base class so you plug in your own strategy while reusing the order and event logic.

## Architecture

### `src/` layout

`src/` is the package root. The editable install adds it to `sys.path`, so you import by package name, not by `src`:

```python
from events.order_tracker import OrderTracker  # OK
from src.events.order_tracker import OrderTracker  # Don't
```

### What lives where

- **helpers** – Calculations, market data helpers, and historical data fetching. Shared logic used by strategies and listeners.
- **events** – Event dispatcher, order tracker, and the `Order` domain model. Handles placing orders and notifying when their status changes.
- **bot_files** – Context object, event listeners, and the base trading bot class. `trading_bot_example.py` is a concrete strategy that buys and sells at a target profit.

### Project structure

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

`bot_main.py` uses `TradingBotExample`. To run a custom strategy, import it from `bot_files` and instantiate it yourself.

## Imports

Always use the installed package names. Never prefix with `src`:

```python
from helpers.calculations import convert_quote_to_base
from events.order_tracker import OrderTracker
from bot_files.context import BotContext
```

Because `pip install -e .` puts `src/` on `sys.path`, Python sees `helpers`, `events`, and `bot_files` as top-level packages.
