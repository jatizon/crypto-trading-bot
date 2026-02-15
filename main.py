import ccxt
import os
from dotenv import load_dotenv
from get_historical_data import get_historical_data
from market_data import *
from wallet import Wallet
from trading_bot import TradingBot
from event_dispatcher import EventDispatcher
from order_tracker import OrderTracker
from context import BotContext


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
bot = TradingBot(context)
bot.run()