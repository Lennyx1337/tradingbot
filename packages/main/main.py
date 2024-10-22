import sys
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from pydantic import BaseModel
sys.path.append('C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages')
sys.path.append('Z:/Python_Projekte/tradingbot/packages')
from utils import util_functions

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class RSIRequest(BaseModel):
    minutes: int
    window_days: int

class FibonacciRequest(BaseModel):
    minutes: int

class EMARequest(BaseModel):
    minutes: int
    period: int

class MACDRequest(BaseModel):
    minutes: int
    short_ema: int
    long_ema: int
    signal_window: int = 9

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        if self.connection:
            await self.connection.send_text(message)

# manager = WebSocketManager()

# @app.websocket('/ws_low_risk')
# async def start_low_risk_strat(websocket:WebSocket):
#     await manager.connect(websocket=WebSocket)
#     try:
#         while True:
#             await websocket.receive_text()        
#     except WebSocketDisconnect:
#         manager.disconnect()



def get_macd_line_list(minutes:int, short_ema: int, long_ema:int):
    if not short_ema < long_ema:
        raise ValueError(f'The short-ema Value: {short_ema} is not taller than the long-ema Value: {long_ema}')
    
    data = util_functions.get_latest_data(minutes)
    result = util_functions.calculate_macd(data, short_ema, long_ema)

    return result

@app.post('/fibonacci')
async def get_fib_retracement(request: FibonacciRequest) -> Dict[str, Any]:
    data = util_functions.get_latest_data(request.minutes)
    if not data:
        raise HTTPException(status_code=404, detail="Keine Daten gefunden.")
    lowest_price = min(data)
    highest_price = max(data)
    fib_levels = util_functions.calculate_fibonacci_retracement(low_price=lowest_price, high_price=highest_price)
    return {'Fibonacci Levels': {'0.382': fib_levels[0], '0.500': fib_levels[1], '0.618': fib_levels[2]}}

@app.post('/ema')
async def get_ema(request: EMARequest) -> Dict[str, Any]:
    data = util_functions.get_latest_data(request.minutes)
    if not data:
        raise HTTPException(status_code=404, detail="No data found.")
    ema_values = util_functions.calculate_ema(data, request.period)
    return {'ema_values': [{'index': i, 'value': value} for i, value in enumerate(ema_values)]}

@app.post('/macd-line')
async def get_macd_line(request: MACDRequest) -> Dict[str, Any]:
    if not request.short_ema < request.long_ema:
        raise HTTPException(status_code=400, detail="Der Wert für short_ema muss kleiner als der für long_ema sein.")
    data = util_functions.get_latest_data(request.minutes)
    macd_line_values = util_functions.calculate_macd(data, request.short_ema, request.long_ema)
    return {'macd_line_values': [{'index': i, 'value': value} for i, value in enumerate(macd_line_values)]}

@app.post('/macd-signal-line')
async def get_macd_signal_line(request: MACDRequest) -> Dict[str, Any]:
    macd_line = get_macd_line_list(request.minutes, request.short_ema, request.long_ema)
    signal_line_values = util_functions.calculate_signal_line(macd_line, request.signal_window)
    return {'macd_signal_line_values': [{'index': i, 'value': value} for i, value in enumerate(signal_line_values)]}

@app.post('/macd-signals-list')
async def get_macd_signals_list(request: MACDRequest) -> Dict[str, Any]:
    macd_line = get_macd_line_list(request.minutes, request.short_ema, request.long_ema)
    macd_signal_line = util_functions.calculate_signal_line(macd_line, request.signal_window)
    signals = util_functions.calculate_signals(macd_line, macd_signal_line)
    return {'signals_values': [{'index': i, 'value': value} for i, value in enumerate(signals)]}


@app.post('/rsi')
async def get_rsi(request: RSIRequest):
    try:
        window_days = int(request.window_days)
        data = util_functions.get_latest_data(request.minutes)
        rsi_value = util_functions.calculate_rsi(data, window_days)
        return {"rsi": rsi_value}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input for window_days. Must be an integer.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

