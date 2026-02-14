import ccxt
import os
from dotenv import load_dotenv
from get_historical_data import get_historical_data
from market_data import *
from wallet import Wallet
from day_trading_bot import DayTradingBot
from event_dispatcher import EventDispatcher
from order_tracker import OrderTracker


load_dotenv()

bot_config = {
    "symbol": "BTC/USDC",
    "type": "market",
    "side": "buy",
    "amount": 1,
    "price": None,
}

exchange = ccxt.coinbase({
    "apiKey": os.getenv("COINBASE_API_KEY"),
    "secret": os.getenv("COINBASE_API_SECRET"),
    "enableRateLimit": True,
})

exchange.options['createMarketBuyOrderRequiresPrice'] = False

dispatcher = EventDispatcher()
order_tracker = OrderTracker(exchange)

bot = DayTradingBot(exchange, dispatcher, order_tracker, bot_config)
bot.run()