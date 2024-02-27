import sys
from flask import jsonify, request
sys.path.append('C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages')
sys.path.append('Z:/Python_Projekte/tradingbot/packages')
sys.path.append('Z:/Python_Projekte/tradingbot')
from utils import util_functions

from tradingbot import app

@app.route('/tradingbot/main/fib', methods=["POST"])
def get_fib_retracement():
    requested_data = request.get_json()
    minutes = requested_data.get('minutes')
    data = util_functions.get_latest_data(minutes)
    lowest_price = min(data)
    highest_price = max(data)
    fib_levels = util_functions.calculate_fibonacci_retracement(low_price=lowest_price, high_price=highest_price)
    result = jsonify({'Fibonacci Levels': [{'0.382': fib_levels[0]}, {'0.500': fib_levels[1]}, {'0.618': fib_levels[2]}]})
    return result

@app.route('/tradingbot/main/ema', methods=["GET"])
def get_ema(minutes: int, ema: int):
    data = util_functions.get_latest_data(minutes)
    result = util_functions.calculate_ema(data, ema)
    return result

@app.route('/tradingbot/main/macd-line', methods=["GET"])
def get_macd_line(minutes:int, short_ema: int, long_ema:int):
    if not short_ema < long_ema:
        raise ValueError(f'The short-ema Value: {short_ema} is not taller than the long-ema Value: {long_ema}')
    data = util_functions.get_latest_data(minutes)
    result = util_functions.calculate_macd(data, short_ema, long_ema)
    return result

@app.route('/tradingbot/main/macd-signal-line', methods=["GET"])
def get_macd_signal_line(minutes: int, short_ema: int, long_ema: int, signal_window: int=9):
    macd_line = get_macd_line(minutes, short_ema, long_ema)
    result = util_functions.calculate_signal_line(macd_line, signal_window)
    return result

@app.route('/tradingbot/main/macd-signals', methods=["GET"])
def get_macd_signals_list(minutes: int, short_ema: int, long_ema: int, signal_window: int=9):
    macd_line = get_macd_line(minutes, short_ema, long_ema)
    macd_signal_line = util_functions.calculate_signal_line(macd_line, signal_window)
    result = util_functions.calculate_signals(macd_line, macd_signal_line)
    return result 

@app.route('/tradingbot/main/rsi', methods=["GET"])
def get_rsi(minutes: int, window_days: int=14):
    data = util_functions.get_latest_data(minutes)
    rsi = util_functions.calculate_rsi(data, window_days)
    return rsi
