import ccxt
import os
from dotenv import load_dotenv
from get_historical_data import get_historical_data
import market_data
import wallet
import day_trading_bot


load_dotenv()

exchange = ccxt.coinbase({
    "apiKey": os.getenv("COINBASE_API_KEY"),
    "secret": os.getenv("COINBASE_API_SECRET"),
    "enableRateLimit": True,
})


get_historical_data(exchange, "BTC/USDC", "1h", use_existing=True)

symbol = "BTC/USDC"

market_data.calculate_total_fee(exchange, "BTC/USDC", 1, "market")

# Instantiate and run the bot (commented out to avoid infinite loop)
bot = day_trading_bot.DayTradingBot(exchange, market_data, wallet)
# bot.run()
