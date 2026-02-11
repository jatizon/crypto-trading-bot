import ccxt
import os
from dotenv import load_dotenv
import market_data
import wallet
import day_trading_bot

load_dotenv()

exchange = ccxt.coinbase({
    "apiKey": os.getenv("COINBASE_API_KEY"),
    "secret": os.getenv("COINBASE_API_SECRET"),
    "enableRateLimit": True,
})

print("Instantiating bot...")
try:
    bot = day_trading_bot.DayTradingBot(exchange, market_data, wallet)
    print("Bot instantiated successfully.")
    print(f"Bot symbol: {bot.symbol}")
    print(f"Bot wallet module: {bot.wallet}")
except Exception as e:
    print(f"Failed to instantiate bot: {e}")

print("Verifying fee calculation...")
try:
    fee = market_data.calculate_total_fee(exchange, "BTC/USDC", 1, "market")
    print(f"Fee calculated: {fee}")
except Exception as e:
    print(f"Failed to calculate fee: {e}")
