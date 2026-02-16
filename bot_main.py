import ccxt
import os
from dotenv import load_dotenv
from helpers.get_historical_data import get_historical_data
from helpers.market_data import *
from bot_files.trading_bot_example import TradingBotExample
from events.event_dispatcher import EventDispatcher
from events.order_tracker import OrderTracker
from bot_files.context import BotContext


load_dotenv()


bot_config = {
    "symbol": "BTC/BRL",
    "type": "market",
    "side": "buy",
    "amount": 15,
    "price": None,
    "profit_percentage": 0.005,
}

exchange = ccxt.binance({
    "apiKey": os.getenv("BINANCE_API_KEY"),
    "secret": os.getenv("BINANCE_API_SECRET"),
    "enableRateLimit": True,
})

exchange.options['createMarketBuyOrderRequiresPrice'] = False

dispatcher = EventDispatcher()
order_tracker = OrderTracker(exchange)
wallet = {"runtime_balances": {"BRL": 100, "BTC": 0}, "profit": 0}

context = BotContext(exchange, dispatcher, order_tracker, bot_config, wallet)
bot = TradingBotExample(context)
bot.run()
