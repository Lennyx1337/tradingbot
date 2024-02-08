import websocket
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# Historische Daten ab dem 01.01.2024
start_time = datetime(2024, 1, 1).timestamp() * 1000

# Websocket-Endpunkt für Live-Daten
live_endpoint = 'wss://stream.binance.com:9443/ws/btcusdt@miniTicker'
historical_endpoint = f'wss://stream.binance.com:9443/ws/btcusdt@kline_1m'

our_msg = json.dumps({'method': 'SUBSCRIBE', 'params': ['btcusdt@miniTicker'], 'id': 1})
df = pd.DataFrame()

fig, ax = plt.subplots()

def animate(i):
    global df
    ax.clear()
    ax.plot(df.index, df['price'], label='BTC Price')
    ax.legend()
    ax.set_title('Live BTC Price')

def on_message(ws, message):
    global df
    data = json.loads(message)
    if 'c' in data:
        price = float(data['c'])
        timestamp = pd.to_datetime(data['E'], unit='ms')
        new_data = pd.DataFrame({'price': [price]}, index=[timestamp])
        df = pd.concat([df, new_data])
        df = df.tail(100)  # Keep only the last 100 data points for visualization

def on_error(ws, error):
    print(f"Fehler: {error}")

def on_close(ws):
    print("WebSocket-Verbindung geschlossen")

def on_open(ws):
    print("WebSocket-Verbindung geöffnet. BTCUSDT Mini-Ticker Stream.")
    ws.send(our_msg)

if __name__ == "__main__":
    # Verbindung für historische Daten
    ws_historical = websocket.WebSocketApp(historical_endpoint,
                                           on_message=on_message,
                                           on_error=on_error,
                                           on_close=on_close)

    # Verbindung für Live-Daten
    ws_live = websocket.WebSocketApp(live_endpoint,
                                      on_message=on_message,
                                      on_error=on_error,
                                      on_close=on_close)

    ws_historical.on_open = lambda ws_historical: ws_historical.send(json.dumps(
        {"method": "SUBSCRIBE", "params": ["btcusdt@kline_1m"], "id": 1}))

    ws_live.on_open = on_open

    ws_live.run_forever()
    ws_historical.run_forever()

    ani = FuncAnimation(fig, animate, interval=10000, save_count=100)  # Aktualisierung alle 10 Sekunden
    plt.show()
