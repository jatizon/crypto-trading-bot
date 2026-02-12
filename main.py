import ccxt
import os
from dotenv import load_dotenv
from get_historical_data import get_historical_data
from market_data *
from wallet import Wallet
from day_trading_bot import DayTradingBot
from event_dispatcher import EventDispatcher


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

dispatcher = event_dispatcher.EventDispatcher()

bot = DayTradingBot(exchange, dispatcher, bot_config)
bot.run()