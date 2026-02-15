import ccxt
import os
from dotenv import load_dotenv
import requests
import time
from tqdm import tqdm
import pandas as pd



def get_historical_data(exchange, symbol, timeframe, since, limit=1000, use_existing=False):
    if use_existing and os.path.exists("data.csv"):
        return pd.read_csv("data.csv")

    since = int(time.mktime(time.strptime(since, '%Y-%m-%d')) * 1000)
    all_ohlcv = []

    # Primeiro chunk
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    if not ohlcv:
        return pd.DataFrame()  # Nenhum dado

    all_ohlcv += ohlcv
    since = ohlcv[-1][0] + 1

    # Calcula delta t do primeiro chunk
    delta_t = ohlcv[-1][0] - ohlcv[0][0]

    # Estima número de chunks total
    timestamp_now = int(time.time() * 1000)
    total_chunks_estimate = max(1, (timestamp_now - ohlcv[0][0]) // delta_t)

    # Inicializa barra de progresso
    pbar = tqdm(total=total_chunks_estimate, desc=f'Fetching {symbol} data', unit='chunk')
    pbar.update(1)  # Já baixamos o primeiro chunk

    # Baixa os chunks restantes
    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        if not ohlcv:
            break

        all_ohlcv += ohlcv
        since = ohlcv[-1][0] + 1

        pbar.update(1)

    pbar.close()

    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)


    df.to_csv("data.csv")
    return df

