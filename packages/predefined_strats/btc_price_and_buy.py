import websocket
import json
import pandas as pd

endpoint = 'wss://stream.binance.com:9443/ws/btcusdt@miniTicker'
our_msg = json.dumps({'method': 'SUBSCRIBE', 'params': ['btcusdt@ticker'], 'id': 1})
df = pd.DataFrame()
in_position = False
buy_orders, sell_orders = [], []

def on_open(ws):
    print("WebSocket Verbindung hergestellt")
    ws.send(our_msg)

def on_message(ws, message):
    global df, in_position, buy_orders, sell_orders
    data = json.loads(message)
    if 's' in data and data['s'] == 'BTCUSDT':
        data = pd.DataFrame({'price':float(data['c'])}, index=[pd.to_datetime(data['E'], unit='ms')])
        df = pd.concat([df, data], axis=0)
        print(df)
        df = df.tail(5)
        last_price = df.tail(1).price.values[0]
        sma_5 = df.price.rolling(5).mean().tail(1).values[0]
        if not in_position and last_price > sma_5:
            print('bought for '+ str(last_price))
            buy_orders.append(last_price)
            in_position = True
        if in_position and sma_5 > last_price:
            print(f'sold for '+ str(last_price))
            print(f'profit: {str(last_price-buy_orders[-1])}')
            sell_orders.append(last_price)

def on_error(ws, error):
    print(f"Fehler: {error}")

def on_close(ws):
    print("WebSocket-Verbindung geschlossen")

def on_open(ws):
    print("WebSocket-Verbindung geöffnet. BTCUSDT Mini-Ticker Stream.")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(endpoint,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

ws.run_forever()