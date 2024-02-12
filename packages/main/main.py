import sys
sys.path.append('C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages')
sys.path.append('Z:/Python_Projekte/tradingbot/packages')
from utils import util_functions

def get_fib_retracement(minutes: int):
    data = util_functions.get_latest_data(minutes)
    lowest_price = min(data)
    highest_price = max(data)
    result = util_functions.calculate_fibonacci_retracement(low_price=lowest_price, high_price=highest_price)
    return result

def get_ema(minutes: int, ema: int):
    data = util_functions.get_latest_data(minutes)
    result = util_functions.calculate_ema(data, ema)
    return result

def get_macd_line(minutes:int, short_ema: int, long_ema:int):
    if not short_ema < long_ema:
        raise ValueError(f'The short-ema Value: {short_ema} is not taller than the long-ema Value: {long_ema}')
    data = util_functions.get_latest_data(minutes)
    result = util_functions.calculate_macd(data, short_ema, long_ema)
    return result

def get_macd_signal_line(minutes: int, short_ema: int, long_ema: int, signal_window: int=9):
    macd_line = get_macd_line(minutes, short_ema, long_ema)
    result = util_functions.calculate_signal_line(macd_line, signal_window)
    return result

def get_macd_signals_list(minutes: int, short_ema: int, long_ema: int, signal_window: int=9):
    macd_line = get_macd_line(minutes, short_ema, long_ema)
    macd_signal_line = util_functions.calculate_signal_line(macd_line, signal_window)
    result = util_functions.calculate_signals(macd_line, macd_signal_line)
    return result 

def get_rsi(minutes: int, window_days: int=14):
    data = util_functions.get_latest_data(minutes)
    rsi = util_functions.calculate_rsi(data, window_days)
    return rsi
