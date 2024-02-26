import pandas as pd
from sqlalchemy import create_engine
import numpy as np

engine = create_engine('sqlite:///Z:/Python_Projekte/tradingbot/packages/getdata/tradingbot.db')
# engine = create_engine('sqlite:///C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages/getdata/tradingbot.db')

def calculate_fibonacci_retracement(low_price: int, high_price: int)-> list:
    fib_levels = [0.382, 0.500, 0.618]
    price_movement = high_price - low_price
    retracement_levels = [(high_price-(price_movement*level)) for level in fib_levels]
    return retracement_levels


def calculate_ema(prices: list, window: int)->list:
    ema_values = [prices[0]]
    smoothing_factor = 2/(window + 1) #Berechnung des Glättungsfaktors window bestimmt, welche EMA man möchte z.B. 200er

    for i in range(1, len(prices)):
        ema = (prices[i] - ema_values[-1]) * smoothing_factor + ema_values[-1]
        ema_values.append(ema)
    
    return ema_values


def calculate_macd(prices: list, short_ema_window: int, long_ema_window: int)->list:
    short_ema = calculate_ema(prices, short_ema_window)
    long_ema = calculate_ema(prices, long_ema_window)
    macd_line = [short - long for short, long in zip(short_ema, long_ema)]

    return macd_line


def calculate_signal_line(macd_line: list, signal_window=9)-> list:
    return calculate_ema(macd_line, signal_window)


def calculate_signals(macd_line: list, signal_line: list)-> list: 
    signals = []
    for i in range(len(macd_line)):
        if macd_line[i]>signal_line[i]:
            signals.append("Buy")
        else:
            signals.append("Sell")
    return signals

   
def calculate_rsi(prices:list, window_days: int = 14) -> list:
    gains = []
    losses = []
    for i in range(1, len(prices)):
        price_diff = prices[i] - prices[i-1]
        if price_diff >= 0:
            gains.append(price_diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(price_diff))
    
    avg_gain = sum(gains[:window_days]) / window_days
    avg_loss = sum(losses[:window_days]) / window_days

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1+rs))

    return rsi


def get_latest_data(num_rows: int)-> list[int]:
    global engine
    query = f"SELECT Close FROM BTCUSDT ORDER BY Time DESC LIMIT {num_rows}"
    latest_data = pd.read_sql(query, engine)
    prices = latest_data.values.flatten().astype(int).tolist()
    return prices

