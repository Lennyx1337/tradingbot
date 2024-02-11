import websocket
import json
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

engine = create_engine('sqlite:///tradingbot.db', echo=True)

endpoint = 'wss://stream.binance.com:9443/ws/btcusdt@miniTicker'
our_msg = json.dumps({'method': 'SUBSCRIBE', 'params': ['btcusdt@ticker'], 'id': 1})

last_insert_time = None

def on_message(ws, message):
    global last_insert_time
    # Try to fix that the index is null for new entries
    # with engine.connect() as conn:
    #     query = text("SELECT MAX(index) FROM BTCUSDT")
    #     result = conn.execute(query)
    #     max_index = result.fetchone()[0]
    data = json.loads(message)
    if 's' in data and data['s'] == 'BTCUSDT':
        timestamp = datetime.fromtimestamp(data['E'] / 1000.0)  
        minute_start = timestamp.replace(second=0, microsecond=0)

        if last_insert_time is None or minute_start > last_insert_time:
            last_insert_time = minute_start
            open_price = float(data['o'])
            high_price = float(data['h'])
            low_price = float(data['l'])
            close_price = float(data['c'])
            volume = float(data['v'])
            with engine.connect() as conn:
                sql_statement = text('''
                    INSERT INTO "BTCUSDT" ("Time", "Open", "High", "Low", "Close", "Volume") 
                    VALUES (:timestamp, :open_price, :high_price, :low_price, :close_price, :volume)
                ''')
                insert_data = {
                    # 'index': max_index+1,
                    'timestamp': timestamp,
                    'open_price': open_price,
                    'high_price': high_price,
                    'low_price': low_price,
                    'close_price': close_price,
                    'volume': volume
                }
                conn.execute(sql_statement, insert_data)
                conn.commit()
                print(pd.read_sql('SELECT Time, High, Low FROM BTCUSDT', engine))
                print("BTCUSDT updated...")

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