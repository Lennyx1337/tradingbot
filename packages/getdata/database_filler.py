import pandas as pd 
from pandas.tseries.offsets import MonthEnd
from sqlalchemy import create_engine
from binance.client import Client
from time import sleep

client = Client()
engine = create_engine('sqlite:///tradingbot.db')

def getdata(symbol, start):
    end = str(pd.to_datetime(start) + MonthEnd(0))
    frame = pd.DataFrame(client.get_historical_klines(symbol,'1m', start, end))
    
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame.set_index = pd.to_datetime(frame.index, unit = 'ms')
    frame = frame.astype(float)
    return frame 

print(getdata('BTCUSDT', '2024-02-09'))

coins = ('BTCUSDT', 'ETHUSDT')
daterange = pd.date_range('2024-01-01', pd.to_datetime('today'), freq='MS')

for coin in coins:
    for date in daterange:
        print(f'processing {date.month_name()} for {coin}...')
        df = getdata(coin, str(date))
        df.to_sql(coin, engine, if_exists='append', index=True)
        sleep(60)
    print(f'finished loading the data for {coin}')

for i in range(10):
    sleep(5)
    print(i)
