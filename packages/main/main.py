import sys
import uvicorn
from fastapi import FastAPI, Request
from typing import Dict, Any
sys.path.append('C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages')
sys.path.append('Z:/Python_Projekte/tradingbot/packages')
from utils import util_functions

app = FastAPI()

@app.post('/fibonacci')
async def get_fib_retracement(request: Request) -> Dict[str, Any]:
    requested_data = await request.get_json()
    minutes = requested_data.get('minutes')
    data = util_functions.get_latest_data(minutes)
    lowest_price = min(data)
    highest_price = max(data)

    fib_levels = util_functions.calculate_fibonacci_retracement(low_price=lowest_price, high_price=highest_price)
    result = {
        'Fibonacci Levels': {
            '0.382': fib_levels[0], 
            '0.500': fib_levels[1], 
            '0.618': fib_levels[2]
            }
        }
    
    return result


@app.get('/ema')
async def get_ema(request: Request)-> Dict[str, Any]:
    requested_data = await request.get_json()
    minutes = requested_data.get('minutes')
    ema = requested_data.get('ema')
    data = util_functions.get_latest_data(minutes)

    ema_values = util_functions.calculate_ema(data, ema)
    ema_json = [{'index': i, 'value': value} for i, value in enumerate(ema_values)]
    result = {
        'ema_values': ema_json
    }

    return result


@app.get('/macd-line')
async def get_macd_line(request: Request) -> Dict[str, Any]:
    requested_data = await request.get_json()
    minutes = requested_data.get('minutes')
    short_ema = requested_data.get('short_ema')
    long_ema = requested_data.get('long_ema')
    if not short_ema < long_ema:
        raise ValueError(f'The short-ema Value: {short_ema} is not taller than the long-ema Value: {long_ema}')
    
    data = util_functions.get_latest_data(minutes)
    macd_line_values = util_functions.calculate_macd(data, short_ema, long_ema)
    macd_line_values_json = [{'index': i, 'value': value} for i, value in enumerate(macd_line_values)]
    result = {
        'macd_line_values': macd_line_values_json
        }
    
    return result

def get_macd_line_list(minutes:int, short_ema: int, long_ema:int):
    if not short_ema < long_ema:
        raise ValueError(f'The short-ema Value: {short_ema} is not taller than the long-ema Value: {long_ema}')
    
    data = util_functions.get_latest_data(minutes)
    result = util_functions.calculate_macd(data, short_ema, long_ema)

    return result

@app.get('/macd-signal-line')
async def get_macd_signal_line(request: Request)-> Dict[str, Any]:
    requested_data = await request.get_json()
    minutes = requested_data.get('minutes')
    short_ema = requested_data.get('short_ema')
    long_ema = requested_data.get('long_ema')
    signal_window = requested_data.get('signal_window')

    if signal_window is None:
        signal_window = 9

    macd_line = get_macd_line_list(minutes, short_ema, long_ema)
    signal_line_values = util_functions.calculate_signal_line(macd_line, signal_window)
    signal_line_values_json = [{'index': i, 'value': value} for i, value in enumerate(signal_line_values)]
    result = {
        'macd_signal_line_values': signal_line_values_json
    }

    return result


@app.get('/macd-signals-list')
async def get_macd_signals_list(request: Request) -> Dict[str, Any]:
    requested_data = await request.get_json()
    minutes = requested_data.get('minutes')
    short_ema = requested_data.get('short_ema')
    long_ema = requested_data.get('long_ema')
    signal_window = requested_data.get('signal_window')

    if signal_window is None:
        signal_window = 9

    macd_line = get_macd_line_list(minutes, short_ema, long_ema)
    macd_signal_line = util_functions.calculate_signal_line(macd_line, signal_window)

    signals = util_functions.calculate_signals(macd_line, macd_signal_line)
    signals_values_json = [{'index': i, 'value': value} for i, value in enumerate(signals)]

    result = {
        'signals_values': signals_values_json
    }

    return result 

@app.get('/rsi')
async def get_rsi(request: Request)-> Dict[str, Any]:
    requested_data = await request.get_json()
    minutes = requested_data.get('minutes')
    window_days = requested_data.get('window_days')
    
    if window_days is None:
        window_days = 14
    data = util_functions.get_latest_data(minutes)
    rsi_value = util_functions.calculate_rsi(data, window_days)
    result = {
        'rsi_value': rsi_value
    }

    return result

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port='8000', reload=True)